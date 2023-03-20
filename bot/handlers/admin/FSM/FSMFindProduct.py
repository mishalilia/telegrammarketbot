from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from bot.database import get_product_by_id, get_product_by_link, Db
from bot.keyboards import cancel_admin_kb, admin_kb, product_method_kb
import bot


class FSMFindProduct(StatesGroup):
    method = State()
    id_link = State()


async def fp_start(message: Message):
    await FSMFindProduct.method.set()
    await bot.bot.send_message(message.from_user.id, "Выберите метод нахождения", reply_markup=product_method_kb)


async def fp_load_method(message: Message, state: FSMContext):
    if message.text.lower() in ["по айди", "по ссылке"]:
        async with state.proxy() as data:
            data["method"] = message.text
        await FSMFindProduct.next()
        if message.text == "По айди":
            await bot.bot.send_message(message.from_user.id, "Отправьте айди", reply_markup=cancel_admin_kb)
        elif message.text == "По ссылке":
            await bot.bot.send_message(message.from_user.id, "Отправьте ссылку", reply_markup=cancel_admin_kb)


async def fp_load_id_link(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["id_link"] = message.text
    db = Db()
    if data["method"] == "По айди":
        product = get_product_by_id(db, data["id_link"])
    else:
        product = get_product_by_link(db, data["id_link"])
    if product is None:
        await bot.bot.send_message(message.from_user.id, "❌ Товара с таким айди не найдено.", reply_markup=admin_kb)
    else:
        await bot.bot.send_message(message.from_user.id,
                                   f"Айди: {product.product_id}\nСсылка: kream.co.kr/products/{product.link}",
                                   reply_markup=admin_kb)
    await state.finish()
