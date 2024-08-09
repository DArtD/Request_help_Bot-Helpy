from dotenv import load_dotenv
from os import getenv
from psycopg2 import connect, Error

load_dotenv()
user = getenv("BASE_USER")
password = getenv("BASE_PASSWORD")
host = getenv("BASE_HOST")
port = getenv("BASE_PORT")


async def check_conn():
    try:
        connection = connect(user=user,
                             password=password,
                             database="bot_logs",
                             host=host,
                             port=port)
        print("Connection success")
    except(Exception, Error) as error:
        print("PostgreSQL error", error)


async def conn():
    connection = connect(user=user,
                         password=password,
                         database="bot_logs",
                         host=host,
                         port=port)

    cursor = connection.cursor()
    return cursor
