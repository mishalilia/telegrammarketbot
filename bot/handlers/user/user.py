import bot
from aiogram.dispatcher import FSMContext
from bot.keyboards import user_kb
from aiogram import Dispatcher
from aiogram.types import Message
from bot.handlers.user.FSM import *


async def start(message: Message):
    await bot.bot.send_message(message.from_user.id, "🌐 Главное меню", reply_markup=user_kb)


async def cancel_fsm(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await start(message)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")

    # cancel FSM
    dp.register_message_handler(cancel_fsm, state="*", text="❌ Отмена")

    # FSM make order
    dp.register_message_handler(mo_start, text="🛒 Сделать заказ", state=None)
    dp.register_message_handler(mo_load_size, state=FSMAddOrder.size)
    dp.register_message_handler(mo_load_product_id, state=FSMAddOrder.product_id)
    dp.register_message_handler(mo_load_location, state=FSMAddOrder.location, content_types=["location", "text"])
