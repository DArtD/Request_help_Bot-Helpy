import logging
import aiogram
from os import getenv
from dotenv import load_dotenv
from utils.base_connect import base_connect

load_dotenv()
chat_id = getenv("CHAT_ID")


async def on_startup(bot: aiogram.Bot):
    try:
        await bot.send_message(chat_id=chat_id, text="Бот Запущен и готов к работе")

    except Exception as err:
        logging.exception(err)


async def on_shutdown(bot: aiogram.Bot):
    try:
        await bot.send_message(chat_id=chat_id, text="Бот Остановлен")

    except Exception as err:
        logging.exception(err)


