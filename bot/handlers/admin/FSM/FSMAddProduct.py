from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from bot.database import db
from bot.keyboards import cancel_admin_kb, admin_kb
import bot


class FSMAddProduct(StatesGroup):
    id = State()
    link = State()


async def ap_start(message: Message):
    await FSMAddProduct.id.set()
    await bot.bot.send_message(message.from_user.id, "➡️ Отправьте айди товара",
                               reply_markup=cancel_admin_kb)


async def ap_load_id(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["id"] = message.text

    await FSMAddProduct.next()
    await bot.bot.send_message(message.from_user.id, "➡️ Отправьте ссылку на товар")


async def ap_load_link(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["link"] = message.text[message.text.find("https"):]

    await bot.bot.send_message(message.from_user.id, db.add_product(data["id"], data["link"]), reply_markup=admin_kb)

    await state.finish()
