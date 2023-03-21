from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from bot.database import db
from bot.keyboards import cancel_user_kb, user_kb, location_kb
from bot.misc import get_sizes
import bot
import uuid


class FSMAddOrder(StatesGroup):
    size = State()
    product_id = State()
    location = State()


async def mo_start(message: Message):
    await FSMAddOrder.size.set()
    await bot.bot.send_message(message.from_user.id, "👞 Введите корейский размер обуви. (220 - 320)",
                               reply_markup=cancel_user_kb)


async def mo_load_size(message: Message, state: FSMContext):
    if message.text.isdigit() and 220 <= int(message.text) <= 320\
            and (int(message.text) % 10 == 0 or int(message.text) % 10 == 5):

        async with state.proxy() as data:
            data["size"] = message.text
        await FSMAddOrder.next()
        await bot.bot.send_message(message.from_user.id, "➡️ Введите айди товара.")

    else:
        await bot.bot.send_message(message.from_user.id, "❌ Некорректный размер.")


async def mo_load_product_id(message: Message, state: FSMContext):
    product = db.get_product_by_id(message.text)

    if product is None:
        await bot.bot.send_message(message.from_user.id, "❌ Товара с таким айди не найдено.")

    else:
        async with state.proxy() as data:

            loading_msg = await bot.bot.send_message(message.from_user.id, "Загрузка...")

            if get_sizes(data["size"], product.link):
                data["product_id"] = product.product_id
                await FSMAddOrder.next()
                await bot.bot.send_message(message.from_user.id, "✈️ Введите адрес доставки.", reply_markup=location_kb)

            else:
                await state.finish()
                await bot.bot.send_message(message.from_user.id, "❌ Нет в наличии.", reply_markup=user_kb)

            await loading_msg.delete()


async def mo_load_location(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == "text":
            data["location"] = f"text:{message.text}"
        else:
            data["location"] = f"location:{message.location.latitude};{message.location.longitude}"

        order_id = str(uuid.uuid1()).replace("-", "")

        if db.add_order(order_id, message.from_user.id, data["product_id"], data["size"], data["location"]):
            print(f"Добавил заказ:\norder_id: {order_id}\nuser_id: {message.from_user.id}"
                  f"\nproduct_id: {data['product_id']}"
                  f"\nsize: {data['size']}\nlocation: {data['location']}")
            await bot.bot.send_message(message.from_user.id, "🕒 Ожидайте, с вами свяжется наш консультант.",
                                       reply_markup=user_kb)

        else:
            print(f"Не удалось добавить заказ:\nuser_id: {message.from_user.id}\nproduct_id: {data['product_id']}"
                  f"\nsize: {data['size']}\nlocation: {data['location']}")
            await bot.bot.send_message(message.from_user.id, "❌ Возникла непредвиденная ошибка. Попробуйте позже.",
                                       reply_markup=user_kb)

        await state.finish()
