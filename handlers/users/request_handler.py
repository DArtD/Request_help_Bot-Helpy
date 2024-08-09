from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from states.request_states import RequestCreation
from dotenv import load_dotenv
from os import getenv
from psycopg2 import connect

load_dotenv()
chat_id = getenv("CHAT_ID")
user = getenv("BASE_USER")
password = getenv("BASE_PASSWORD")
host = getenv("BASE_HOST")
port = getenv("BASE_PORT")
router = Router()


@router.message(F.text == "Отправить заявку")
async def req_creation(message: Message, state: FSMContext):
    await message.answer("Опишите вашу проблему")
    await state.set_state(RequestCreation.req_waiting)


@router.message(F.text, StateFilter(RequestCreation.req_waiting))
async def req_sending(message: Message, state: FSMContext):
    connection = connect(user=user,
                         password=password,
                         host=host,
                         port=port,
                         database='bot_logs')
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM users WHERE user_id={message.from_user.id}')
    user_info = cursor.fetchone()
    await message.bot.send_message(chat_id=chat_id, text=f'Заявка от пользователя: @{message.from_user.username}\n'
                                                         f'{user_info[2]}, {user_info[3]}\n'
                                                         f'{message.text}')

#
# @router.message(F.text)
# async def client_address(message: Message):
#
#     await message.answer("Заявка направлена в IT-отдел")
