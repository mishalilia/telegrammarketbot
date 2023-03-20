from os import getenv
from dotenv import load_dotenv
from .handlers import register_admin_handlers, register_user_handlers
from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=getenv("TOKEN"), parse_mode="HTML")


def on_start(dp: Dispatcher):
    register_user_handlers(dp)
    register_admin_handlers(dp)

    print("Bot has been started.")


def start_bot():
    # loading env
    load_dotenv()

    # starting bot
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=on_start(dp))
