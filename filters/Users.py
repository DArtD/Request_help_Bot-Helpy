from aiogram.types import Message
from aiogram.filters import BaseFilter
from dotenv import load_dotenv
from os import getenv
import psycopg2
from psycopg2 import Error

load_dotenv()
user = getenv("BASE_USER")
password = getenv("BASE_PASSWORD")
host = getenv("BASE_HOST")
port = getenv("BASE_PORT")


class Users(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        try:
            connection = psycopg2.connect(user=user,
                                          # пароль, который указали при установке PostgreSQL
                                          password=password,
                                          host=host,
                                          port=port,
                                          database='bot_logs')

            cursor = connection.cursor()
            cursor.execute('SELECT user_id FROM public.users')
            users_id = cursor.fetchall()
            for i in users_id:
                if message.from_user.id == i[0]:
                    return True

        except(Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)



        # else:
        #     await message.answer('Вас нет в БД')
        #     return False
