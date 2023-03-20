from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


# main user keyboard
make_order = KeyboardButton("🛒 Сделать заказ")

user_kb = ReplyKeyboardMarkup(resize_keyboard=True)
user_kb.add(make_order)
