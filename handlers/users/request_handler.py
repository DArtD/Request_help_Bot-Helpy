from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from states.request_states import RequestCreation
from dotenv import load_dotenv
from os import getenv
from utils.base_connect import conn
from datetime import datetime
from keyboards.inline_kb import cancel_butt, accept_butt, return_butt, req_choice_interaction, admin
from emoji import emojize

load_dotenv()
chat_id = getenv("CHAT_ID")
router = Router()


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


@router.callback_query(F.data == "req_send")
async def req_creation(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text='Подробно опишите проблему', reply_markup=cancel_butt())
    await state.set_state(RequestCreation.req_waiting)


@router.message(F.text, StateFilter(RequestCreation.req_waiting))
async def req_sending(message: Message, state: FSMContext):
    await message.answer(text="Заявка направлена в IT отдел", reply_markup=return_butt())
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO public.users_requests (user_id, req_text, req_date, status) "
                   f"VALUES ({message.from_user.id}, '{message.text}', "
                   f"'{datetime.now().strftime('%d.%m.%Y %H:%M')}', 'active')")
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
    cursor.execute("SELECT users_requests.req_id, users.username, users_requests.req_text, "
                   "users_requests.req_date FROM public.users_requests "
                   "JOIN public.users ON users.user_id = users_requests.user_id WHERE status='active'")
    for i in cursor.fetchall():
        text = (f'ID запроса: {i[0]}\n'
                f'Пользователь: {i[1]}\n'
                f'<b>Описание проблемы:</b> {i[2]}\n'
                f'<u>Дата: {i[3]}</u>')

        await callback.message.answer(text=text, reply_markup=accept_butt())

    connect.commit()
    cursor.close()
    connect.close()

    await callback.answer()


@router.callback_query(F.data == 'accept')
async def req_choice(callback: CallbackQuery):
    text = callback.message.text
    req_id = ''
    for i in range(12, len(text)):
        if text[i] == '\n':
            break
        req_id += text[i]

    await callback.answer()
    connection = await conn()
    cursor = connection.cursor()
    cursor.execute("SELECT users_requests.req_id, users.username, users_requests.req_text, "
                   "users_requests.req_date FROM public.users_requests "
                   f"JOIN public.users ON users.user_id = users_requests.user_id WHERE req_id = {req_id}")
    res = cursor.fetchone()
    text = '<u><b>Что сделать с заявкой?</b></u>\n'
    text += (f'ID запроса: {res[0]}\n'
             f'Пользователь: {res[1]}\n'
             f'<b>Описание проблемы:</b> {res[2]}\n'
             f'<u>Дата: {res[3]}</u>')
    await callback.message.answer(text=text, reply_markup=req_choice_interaction())


@router.callback_query(F.data == 'admin_panel')
async def admin_panel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text=emojize(":warning:") + " Админ панель для избранных " + emojize(":warning:"), reply_markup=admin_panel())
