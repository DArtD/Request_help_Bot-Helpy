from os import getenv
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler


load_dotenv()   # заргужаем в прогу .env
admins = getenv('ADMINS')   # вытягиваем оттуда админов

scheduler = AsyncIOScheduler(timezone='Asia/Yekaterinburg')   # создаем асинхронный планировщик уведомлений

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# настраиваем запись логов
logger = logging.getLogger(__name__)

bot = Bot(token=getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))   # прописываем объект бота
dp = Dispatcher(storage=MemoryStorage())    # позволяем хранить данные в оперативке


#
# async def main():
#     bot = Bot(token=TOKEN)
#     dp = Dispatcher(storage=storage)
#     logging.basicConfig(level=logging.DEBUG)
#     dp.startup.register(on_startup)
#     dp.shutdown.register(on_shutdown)
#     dp.include_routers(rout1, rout2)
#
#     try:
#         await dp.start_polling(bot)
#     finally:
#         await bot.session.close()
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
