import asyncio
from TBot import bot, dp, scheduler
from handlers.start import start_router
from aiogram.types import BotCommand, BotCommandScopeDefault
from dotenv import load_dotenv
from utils.base_connect import conn
# from work_time.time_func import send_time_msg
load_dotenv()


async def set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='id', description='id чата')]
    await bot.set_my_commands(commands, BotCommandScopeDefault)


async def main():
    dp.include_router(start_router)
    await conn()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await set_commands()

if __name__ == "__main__":
    asyncio.run(main())
