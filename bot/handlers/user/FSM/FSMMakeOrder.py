from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from bot.database import db
from bot.keyboards import cancel_user_kb, user_kb, location_kb, more_kb, confirm_kb
from bot.misc import get_price, form_order, get_product_cost
import bot
import uuid


class FSMMakeOrder(StatesGroup):
    product_id = State()
    size = State()
    more = State()
    confirm = State()
    location = State()
    payment = State()
    products = {}
    more_flag = False


async def mo_start(message: Message):
    await FSMMakeOrder.product_id.set()
    await bot.bot.send_message(message.from_user.id, "➡️ Введите айди товара.", reply_markup=cancel_user_kb)


async def mo_load_product_id(message: Message, state: FSMContext):
    product = db.get_product_by_id(message.text)

    if product is None:
        await bot.bot.send_message(message.from_user.id, "❌ Товара с таким айди не найдено.")

    else:
        await FSMMakeOrder.next()
        await bot.bot.send_message(message.from_user.id, "Введите размер.")
        if FSMMakeOrder.products.get(message.from_user.id):
            FSMMakeOrder.products[message.from_user.id].append({"id": product.product_id, "link": product.link})
        else:
            FSMMakeOrder.products[message.from_user.id] = [{"id": product.product_id, "link": product.link}]
        async with state.proxy() as data:
            data["product_id"] = message.text


async def mo_load_size(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["size"] = message.text.upper()

        loading_msg = await bot.bot.send_message(message.from_user.id, "Проверяем наличие размера. "
                                                                       "(Это занимает до 30 секунд)")

        price = await get_price(data["size"], FSMMakeOrder.products[message.from_user.id][-1]["link"])
        await loading_msg.delete()

        current_state = await state.get_state()
        if current_state != "FSMMakeOrder:size":
            return

        if price:
            await FSMMakeOrder.next()
            FSMMakeOrder.products[message.from_user.id][-1]["size"] = data["size"]
            FSMMakeOrder.products[message.from_user.id][-1]["price"] = get_product_cost(float(price) * 1.15 + 5000)
            await bot.bot.send_message(message.from_user.id, "✅ Есть в наличии.")
            await bot.bot.send_message(message.from_user.id, "Желаете добавить еще один товар?", reply_markup=more_kb)

        else:
            del FSMMakeOrder.products[message.from_user.id][-1]
            await bot.bot.send_message(message.from_user.id, "❌ Нет в наличии.", reply_markup=user_kb)
            if len(FSMMakeOrder.products[message.from_user.id]):
                await FSMMakeOrder.next()
                await bot.bot.send_message(message.from_user.id, "Желаете добавить еще один товар?",
                                           reply_markup=more_kb)
            else:
                FSMMakeOrder.more_flag = False
                await state.finish()
                return


async def mo_more(message: Message, state: FSMContext):
    FSMMakeOrder.more_flag = True

    if message.text == "➕ Добавить ещё":
        await mo_start(message)

    elif message.text == "🙅🏻‍♂️ Нет":
        await FSMMakeOrder.next()

        loading_msg = await bot.bot.send_message(message.from_user.id, "🕒 Формируем заказ, ожидайте.")
        await bot.bot.send_message(message.from_user.id, form_order(FSMMakeOrder.products[message.from_user.id]), reply_markup=confirm_kb)
        await loading_msg.delete()


async def mo_confirm(message: Message, state: FSMContext):
    if message.text == "✅ Подтвердить":
        await FSMMakeOrder.next()
        await bot.bot.send_message(message.from_user.id,
                                   "✈️ Введите адрес доставки. (Отправьте локацию"
                                   " или введите вручную в формате: Г. Москва, Профсоюзная"
                                   " ул., д. 43к2, кв. 7, 117420)",
                                   reply_markup=location_kb)


async def mo_load_location(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == "text":
            data["location"] = f"text:{message.text}"
        else:
            data["location"] = f"location:{message.location.latitude};{message.location.longitude}"

        text = "Мы внесли все данные в базу ☑️\n" \
               "Для завершения оформления, пожалуйста оплатите общую сумму заказа по следующим реквизитам:\n" \
               "NBU (Узбекистан)\n5614 6819 0087 2932\nANJELIKA LI\n\n" \
               "*Доступны переводы без комиссии через приложения Сбер и Тинькофф\n\nПосле произведения оплаты отправьте ФИО" \
               " отправителя в этот чат, после чего менеджер проверит статус оплаты и свяжется с вами 👨🏻‍💻"
        await bot.bot.send_message(message.from_user.id, text,
                                   reply_markup=cancel_user_kb)

        await FSMMakeOrder.next()


async def mo_payment(message: Message, state: FSMContext):
    async with state.proxy() as data:
        order_id = str(uuid.uuid1()).replace("-", "")
        db.add_order(order_id, message.from_user.id, FSMMakeOrder.products[message.from_user.id], data["location"], message.text)

        await bot.bot.send_message(message.from_user.id, "🕖 Ожидайте. Ваш заказ перешёл к менеджеру."
                                                         " С вами свяжутся в течение суток.",
                                   reply_markup=user_kb)

        del FSMMakeOrder.products[message.from_user.id]
        await state.finish()
