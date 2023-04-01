from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# ADMIN:
# cancel keyboard
cancel_a = KeyboardButton("🚫 Отмена")

cancel_admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_admin_kb.add(cancel_a)

# product by id or link keyboard
by_id = KeyboardButton("По айди")
by_link = KeyboardButton("По ссылке")

product_method_kb = ReplyKeyboardMarkup(resize_keyboard=True)
product_method_kb.add(by_id, by_link).add(cancel_a)


# USER:
# cancel user keyboard
cancel_u = KeyboardButton("❌ Отмена")

cancel_user_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_user_kb.add(cancel_u)

# location keyboard
send_location = KeyboardButton("Отправить локацию", request_location=True)

location_kb = ReplyKeyboardMarkup(resize_keyboard=True)
location_kb.add(send_location).add(cancel_u)

# more keyboard
enough = KeyboardButton("🙅🏻‍♂️ Нет")
more = KeyboardButton("➕ Добавить ещё")

more_kb = ReplyKeyboardMarkup(resize_keyboard=True)
more_kb.add(enough).add(more).add(cancel_u)

# confirm keyboard
confirm = KeyboardButton("✅ Подтвердить")

confirm_kb = ReplyKeyboardMarkup(resize_keyboard=True)
confirm_kb.add(confirm).add(cancel_u)
