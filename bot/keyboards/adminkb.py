from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


back = KeyboardButton("↩️ Назад")

# main admin keyboard
orders = KeyboardButton("📄 Работа с заказами")
products = KeyboardButton("📦 Работа с товарами")
exit_btn = KeyboardButton("🚪 Выход")

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb.add(orders).add(products).add(exit_btn)


# orders keyboard
show_orders = KeyboardButton("📃 Показать заказы")
delete_orders = KeyboardButton("🗑️ Удалить заказ")

orders_kb = ReplyKeyboardMarkup(resize_keyboard=True)
orders_kb.add(show_orders).add(delete_orders).add(back)


# products keyboard
add_product = KeyboardButton("➕ Добавить товар")
delete_product = KeyboardButton("🗑️ Удалить товар")
find_product = KeyboardButton("🔍 Найти товар")

products_kb = ReplyKeyboardMarkup(resize_keyboard=True)
products_kb.add(add_product).add(delete_product, find_product).add(back)
