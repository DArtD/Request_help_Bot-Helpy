import asyncio
from TBot import bot, dp, scheduler
from handlers.start import start_router
from handlers.users.request_handler import req_router
from handlers.users.it_handlers import it_router
from aiogram.types import BotCommand, BotCommandScopeDefault
from dotenv import load_dotenv
from utils.base_connect import check_conn
load_dotenv()


async def set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='id', description='id чата')]
    await bot.set_my_commands(commands, BotCommandScopeDefault)


async def main():
    dp.include_routers(start_router, req_router, it_router)
    await check_conn()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await set_commands()

if __name__ == "__main__":
    asyncio.run(main())
