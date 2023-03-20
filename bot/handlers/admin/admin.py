import bot
from bot.handlers.user import start
from bot.keyboards import admin_kb, orders_kb, products_kb
from bot.misc import is_admin
from aiogram import Dispatcher
from aiogram.types import Message
from bot.handlers.admin.FSM import *
from aiogram.dispatcher import FSMContext
from bot.database import get_all_orders, delete_order
from bot.database import Db


async def admin(message: Message):
    if await is_admin(bot.bot, message.from_user.id):
        await bot.bot.send_message(message.from_user.id, "💻 Админ панель.", reply_markup=admin_kb)
    else:
        await bot.bot.send_message(message.from_user.id, "❌ Вы не являетесь админом.")


async def exit_admin(message: Message):
    if await is_admin(bot.bot, message.from_user.id):
        await start(message)


async def products(message: Message):
    if await is_admin(bot.bot, message.from_user.id):
        await bot.bot.send_message(message.from_user.id, "➡️ Далее...", reply_markup=products_kb)


async def orders(message: Message):
    if await is_admin(bot.bot, message.from_user.id):
        await bot.bot.send_message(message.from_user.id, "➡️ Далее...", reply_markup=orders_kb)


async def back(message: Message):
    if await is_admin(bot.bot, message.from_user.id):
        await bot.bot.send_message(message.from_user.id, "↩️ Назад.", reply_markup=admin_kb)


async def cancel_fsm(message: Message, state: FSMContext):
    if await is_admin(bot.bot, message.from_user.id):
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await admin(message)


async def show_all_orders(message: Message):
    if await is_admin(bot.bot, message.from_user.id):
        db = Db()
        all_orders = get_all_orders(db)

        if len(all_orders) == 0:
            bot.bot.send_message(message.from_user.id, "Заказов нет.")

        for order in all_orders:

            method, location = order.location.split(":")[0], "".join(order.location.split(":")[1:])
            try:
                chat_member = await bot.bot.get_chat_member(order.user_id, order.user_id)
            except Exception:
                # in case user deleted our chat
                delete_order(db, order.order_id)
                continue
            user = chat_member.user

            if method == "text":
                await bot.bot.send_message(message.from_user.id, f"Айди заказа: `{order.order_id}`\n"
                                                                 f"Пользователь: {user.mention}\n"
                                                                 f"Айди товара: {order.product_id}\n"
                                                                 f"Размер: {order.size}\n"
                                                                 f"Адрес: {location}", parse_mode="Markdown")

            else:
                await bot.bot.send_message(message.from_user.id, f"Айди заказа: `{order.order_id}`\n"
                                                                 f"Пользователь: {user.mention}\n"
                                                                 f"Айди товара: {order.product_id}\n"
                                                                 f"Размер: {order.size}\n"
                                                                 f"Адрес: ", parse_mode="Markdown")
                latitude, longitude = float(location.split(";")[0]), float(location.split(";")[1])
                await bot.bot.send_location(message.from_user.id, latitude, longitude)


def register_admin_handlers(dp: Dispatcher):
    # admin access
    dp.register_message_handler(admin, lambda msg: msg.text.lower() in ["admin", "админ", "flvby", "фвьшт"])

    # admin panel
    dp.register_message_handler(exit_admin, text="🚪 Выход")
    dp.register_message_handler(products, text="📦 Работа с товарами")
    dp.register_message_handler(orders, text="📄 Работа с заказами")

    # back to admin panel
    dp.register_message_handler(back, text="↩️ Назад")

    # cancel FSM
    dp.register_message_handler(cancel_fsm, state="*", text="🚫 Отмена")

    # FSM add product
    dp.register_message_handler(ap_start, text="➕ Добавить товар", state=None)
    dp.register_message_handler(ap_load_id, state=FSMAddProduct.id)
    dp.register_message_handler(ap_load_link, state=FSMAddProduct.link)

    # FSM delete product
    dp.register_message_handler(dp_start, text="🗑️ Удалить товар", state=None)
    dp.register_message_handler(dp_load_method, state=FSMDeleteProduct.method)
    dp.register_message_handler(dp_load_id_link, state=FSMDeleteProduct.id_link)

    # FSM find product
    dp.register_message_handler(fp_start, text="🔍 Найти товар", state=None)
    dp.register_message_handler(fp_load_method, state=FSMFindProduct.method)
    dp.register_message_handler(fp_load_id_link, state=FSMFindProduct.id_link)

    # FSM delete order
    dp.register_message_handler(do_start, text="🗑️ Удалить заказ", state=None)
    dp.register_message_handler(do_load_order_id, state=FSMDeleteOrder.order_id)

    # show all orders
    dp.register_message_handler(show_all_orders, text="📃 Показать заказы")
