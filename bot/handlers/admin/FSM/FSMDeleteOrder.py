from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from bot.database import db
from bot.keyboards import cancel_admin_kb, admin_kb
import bot


class FSMDeleteOrder(StatesGroup):
    order_id = State()


async def do_start(message: Message):
    await FSMDeleteOrder.order_id.set()
    await bot.bot.send_message(message.from_user.id, "➡️ Отправьте айди заказа.", reply_markup=cancel_admin_kb)


async def do_load_order_id(message: Message, state: FSMContext):
    await bot.bot.send_message(message.from_user.id, db.delete_order(message.text), reply_markup=admin_kb)
    await state.finish()
