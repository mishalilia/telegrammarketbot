import bot
from aiogram.dispatcher import FSMContext
from bot.keyboards import user_kb, more_kb
from aiogram import Dispatcher
from aiogram.types import Message
from bot.handlers.user.FSM import *


async def start(message: Message):
    await bot.bot.send_message(message.from_user.id, "🌐 Главное меню", reply_markup=user_kb)


async def cancel_fsm(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return

    if ((current_state == "FSMMakeOrder:size" or current_state == "FSMMakeOrder:product_id")
            and FSMMakeOrder.more_flag is False) or (current_state == "FSMMakeOrder:more"):
        await state.finish()
        await start(message)
        FSMMakeOrder.more_flag = False
        FSMMakeOrder.products.clear()

    else:
        await bot.bot.send_message(message.from_user.id, "Желаете добавить еще один товар?", reply_markup=more_kb)
        await FSMMakeOrder.more.set()
        await mo_more(message, state)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")

    # cancel FSM
    dp.register_message_handler(cancel_fsm, state="*", text="❌ Отмена")

    # FSM make order
    dp.register_message_handler(mo_start, text="🛒 Сделать заказ", state=None)
    dp.register_message_handler(mo_load_product_id, state=FSMMakeOrder.product_id)
    dp.register_message_handler(mo_load_size, state=FSMMakeOrder.size)
    dp.register_message_handler(mo_more, state=FSMMakeOrder.more)
    dp.register_message_handler(mo_confirm, state=FSMMakeOrder.confirm)
    dp.register_message_handler(mo_load_location, state=FSMMakeOrder.location, content_types=["location", "text"])
    dp.register_message_handler(mo_payment, state=FSMMakeOrder.payment)
