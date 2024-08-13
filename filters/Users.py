from aiogram.types import Message
from aiogram.filters import BaseFilter
from dotenv import load_dotenv
from os import getenv
from utils.base_connect import conn

load_dotenv()   # подтягиваем все данные из .env
user = getenv("BASE_USER")  # берем нужные переменные
password = getenv("BASE_PASSWORD")
host = getenv("BASE_HOST")
port = getenv("BASE_PORT")


class Users(BaseFilter):    # класс-фильтр

    async def __call__(self, message: Message) -> bool:     # при вызове проверяет наличие пользака в БД
        connection = await conn()                           # позволяет ограничить круг пользователей бота
        cursor = connection.cursor()
        cursor.execute('SELECT user_id FROM public.users')
        users_id = cursor.fetchall()
        for i in users_id:
            if message.from_user.id == i[0]:
                return True

    # else:
    #     await message.answer('Вас нет в БД')
    #     return False
