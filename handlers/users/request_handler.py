from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from states.request_states import RequestCreation
from dotenv import load_dotenv
from os import getenv
from utils.base_connect import conn
from datetime import datetime

load_dotenv()
chat_id = getenv("CHAT_ID")
user = getenv("BASE_USER")
password = getenv("BASE_PASSWORD")
host = getenv("BASE_HOST")
port = getenv("BASE_PORT")
router = Router()


@router.callback_query(F.data == "req_send")
async def req_creation(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Подробно опишите вашу проблему")
    await state.set_state(RequestCreation.req_waiting)


@router.message(F.text == "Данные")
async def user_data(message: Message):
    text = ''
    text += "id: " + str(message.from_user.id) + '\n'
    text += "username: @" + str(message.from_user.username) + '\n'
    text += "first_name: " + str(message.from_user.first_name) + '\n'
    text += "last_name: " + str(message.from_user.last_name) + '\n'
    text += "full_name: " + str(message.from_user.full_name) + '\n'
    text += "is_bot: " + str(message.from_user.is_bot) + '\n'
    text += "premium: " + str(message.from_user.is_premium) + '\n'
    text += "language_code: " + str(message.from_user.language_code) + '\n'
    text += "url: " + str(message.from_user.url) + '\n'
    await message.answer(text=text)


@router.message(F.text, StateFilter(RequestCreation.req_waiting))
async def req_sending(message: Message, state: FSMContext):
    await message.answer("Заявка направлена в IT отдел")
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO public.users_requests (user_id, req_text, req_date, status) "
                   f"VALUES ({message.from_user.id}, '{message.text}', '{datetime.now().strftime('%d.%m.%Y %H:%M')}', 'active')")
    cursor.execute(f'SELECT * FROM users WHERE user_id={message.from_user.id}')
    user_info = cursor.fetchone()
    await message.bot.send_message(chat_id=chat_id, text=f'Заявка от пользователя: @{message.from_user.username}\n'
                                                         f'{user_info[2]}, {user_info[3]}\n'
                                                         f'{message.text}')
    connect.commit()
    cursor.close()
    connect.close()


@router.callback_query(F.data == 'active_req')
async def active_reqs_list(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute("SELECT users_requests.req_id, users.username, users_requests.tel_number, users_requests.req_text, "
                   "users_requests.req_date FROM public.users_requests "
                   "JOIN public.users ON users.user_id = users_requests.user_id WHERE status='active'")
    text = ''
    for i in cursor.fetchall():
        text = (f'ID запроса: {i[0]}\n'
                f'Пользователь: {i[1]}\n'
                f'Тел.: {i[2]}\n'
                f'<b>Описание проблемы:</b> {i[3]}\n'
                f'<u>Дата: {i[4]}</u>')
        await callback.message.answer(text)

    await callback.answer()

    connect.commit()
    cursor.close()
    connect.close()
#
# @router.message(F.text)
# async def client_address(message: Message):
#
#     await message.answer("Заявка направлена в IT-отдел")
