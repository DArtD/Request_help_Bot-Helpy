from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from states.request_states import RequestCreation
from TBot import dp, StorageKey
from dotenv import load_dotenv
from os import getenv
from utils.base_connect import conn
from datetime import datetime
from keyboards.inline_kb import cancel_butt, return_butt, kb_maker, user_req, req_sender, yes_no_kb

load_dotenv()
chat_id = getenv("CHAT_ID")
req_router = Router()


@req_router.message(F.text == "Данные")
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


@req_router.callback_query(F.data == "req_send")
async def req_creation(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text='Подробно опишите проблему', reply_markup=cancel_butt())
    await state.set_state(RequestCreation.req_waiting)


@req_router.message(F.text, StateFilter(RequestCreation.req_waiting))
async def req_sending(message: Message, state: FSMContext):
    await message.answer(text="Заявка направлена в IT отдел", reply_markup=req_sender())
    connect = await conn()
    cursor = connect.cursor()

    cursor.execute(f"INSERT INTO public.users_requests (user_id, req_text, req_date, status) "
                   f"VALUES ({message.from_user.id}, '{message.text}', "
                   f"'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', 'active')")
    cursor.execute(f'SELECT * FROM users WHERE user_id={message.from_user.id}')

    user_info = cursor.fetchone()
    await message.bot.send_message(chat_id=chat_id, text=f'Заявка от пользователя: @{message.from_user.username}\n'
                                                         f'{user_info[2]}, {user_info[3]}\n'
                                                         f'{message.text}')

    connect.commit()
    cursor.close()
    connect.close()


@req_router.callback_query(F.data == 'my_req')
async def my_req(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute("SELECT users_requests.req_id, users.username, users_requests.req_text, "
                   "users_requests.status, users_requests.executive, users_requests.req_date "
                   "FROM public.users_requests "
                   f"JOIN public.users ON users.user_id = users_requests.user_id "
                   f"WHERE users_requests.user_id={callback.from_user.id}")

    if cursor.rowcount > 0:
        req_id = []
        text = ''
        for i in cursor.fetchall():
            req_id.append(i[0])
            text += (f'ID запроса: <b>{i[0]}</b>\n'
                     f'Пользователь: {i[1]}\n'
                     f'<b>Описание проблемы:</b> {i[2]}\n'
                     f'Статус: {i[3]}\n'
                     f'Исполняющий: {i[4]}\n'
                     f'<u>Дата: {i[5]}</u>\n\n')
        await callback.message.edit_text(text=text, reply_markup=kb_maker(req_id, '!'))

    else:
        await callback.message.edit_text(text="Нет активных заявок", reply_markup=return_butt())

    connect.commit()
    cursor.close()
    connect.close()

    await callback.answer()


@req_router.callback_query(F.data.startswith('!'))
async def user_req_choice(callback: CallbackQuery):
    await callback.answer()
    connection = await conn()
    cursor = connection.cursor()
    cursor.execute("SELECT users_requests.req_id, users.username, users_requests.req_text, "
                   "users_requests.executive, users_requests.status, users_requests.req_date "
                   "FROM public.users_requests "
                   f"JOIN public.users ON users.user_id = users_requests.user_id WHERE req_id = {callback.data[1:]}")

    res = cursor.fetchone()
    text = '<u><b>Что сделать с заявкой?</b></u>\n'
    text += (f'ID запроса: {res[0]}\n'
             f'Пользователь: {res[1]}\n'
             f'<b>Описание проблемы:</b> {res[2]}\n'
             f'Исполняющий: {res[3]}\n'
             f'Статус: <u>{res[4]}</u>\n'
             f'<u>Дата: {res[5]}</u>')

    await callback.message.edit_text(text=text, reply_markup=user_req(res[0]))


@req_router.callback_query(F.data.startswith('//'))
async def req_cancel(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"UPDATE users_requests SET status='Закрыта пользователем' WHERE req_id={callback.data[2:]}")
    cursor.execute("SELECT users_requests.req_id, users.username, users_requests.req_text, "
                   "users_requests.executive, users_requests.req_date "
                   "FROM public.users_requests "
                   f"JOIN public.users ON users.user_id = users_requests.user_id WHERE req_id = {callback.data[2:]}")

    res = cursor.fetchone()
    connect.commit()

    text = (f'ID запроса: {res[0]}\n'
            f'Пользователь: {res[1]}\n'
            f'<b>Описание проблемы:</b> {res[2]}\n'
            f'Исполняющий: {res[3]}\n'
            f'<u>Дата: {res[4]}</u>')

    if res[3] is not None:
        cursor.execute(f"SELECT id FROM admins WHERE nickname = '{res[3]}'")
        connect.commit()
        admin_id = cursor.fetchone()
        await callback.bot.send_message(text='<b><u>Заявка закрыта пользователем</u></b>\n' + text, chat_id=admin_id[0])

    await callback.answer()
    await callback.bot.send_message(text='<b><u>Заявка закрыта пользователем</u></b>\n' + text, chat_id=chat_id)
    await callback.message.edit_text(text='Заявка закрыта', reply_markup=return_butt())

    cursor.close()
    connect.close()


@req_router.callback_query(F.data.startswith('user_question'))
async def user_question(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute("SELECT users_requests.req_id, users.username, users_requests.req_text, "
                   "users_requests.executive, users_requests.req_date, users_requests.user_id "
                   "FROM public.users_requests "
                   f"JOIN public.users ON users.user_id = users_requests.user_id WHERE req_id = {callback.data[14:]}")

    res = cursor.fetchone()
    text = ('<u><b>Была ли проблема решена?</b></u>\n'
            '<u><b>Проверьте перед ответом</b></u>\n')
    text += (f'ID запроса: {res[0]}\n'
             f'Пользователь: {res[1]}\n'
             f'<b>Описание проблемы:</b> {res[2]}\n'
             f'Исполняющий: {res[3]}\n'
             f'<u>Дата: {res[4]}</u>')

    await callback.bot.send_message(text=text, chat_id=res[5], reply_markup=yes_no_kb(res[0]))
    await callback.answer()
