from dotenv import load_dotenv
from os import getenv
from psycopg2 import connect, Error

load_dotenv()
user = getenv("BASE_USER")
password = getenv("BASE_PASSWORD")
host = getenv("BASE_HOST")
port = getenv("BASE_PORT")


async def check_conn():     # функция проверки связи с БД
    try:
        connection = connect(user=user,
                             password=password,
                             database="bot_logs",
                             host=host,
                             port=port)
        print("PgSQL: Connection success")
    except (Exception, Error) as error:
        print("PgSQL error", error)


async def conn():           # функция подключения к БД, возвращает объект connection
    connection = connect(user=user,     # connection позволяет делать запрос и сохранять данные в БД
                         password=password,
                         database="bot_logs",
                         host=host,
                         port=port)

    return connection
