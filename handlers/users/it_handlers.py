from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils.base_connect import conn
from keyboards.inline_kb import req_choice_interaction, admin_kb, return_butt, kb_maker
from emoji import emojize

it_router = Router()


@it_router.callback_query(F.data == 'active_req')
async def active_reqs_list(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute("SELECT users_requests.req_id, users.username, users_requests.req_text, "
                   "users_requests.executive, users_requests.req_date FROM public.users_requests "
                   "JOIN public.users ON users.user_id = users_requests.user_id WHERE status='active'")

    if cursor.rowcount > 0:
        req_id = []
        text = ''
        for i in cursor.fetchall():
            req_id.append(i[0])
            text += (f'ID запроса: <b>{i[0]}</b>\n'
                     f'Пользователь: {i[1]}\n'
                     f'<b>Описание проблемы:</b> {i[2]}\n'
                     f'Исполняющий: {i[3]}\n'
                     f'<u>Дата: {i[4]}</u>\n\n')
        await callback.message.edit_text(text=text, reply_markup=kb_maker(req_id))

    else:
        await callback.message.edit_text(text="Нет активных заявок", reply_markup=return_butt())

    connect.commit()
    cursor.close()
    connect.close()

    await callback.answer()


@it_router.callback_query(F.data.isnumeric())
async def req_choice(callback: CallbackQuery):
    await callback.answer()
    connection = await conn()
    cursor = connection.cursor()
    cursor.execute("SELECT users_requests.req_id, users.username, users_requests.req_text, "
                   "users_requests.executive, users_requests.req_date FROM public.users_requests "
                   f"JOIN public.users ON users.user_id = users_requests.user_id WHERE req_id = {callback.data}")

    res = cursor.fetchone()
    text = '<u><b>Что сделать с заявкой?</b></u>\n'
    text += (f'ID запроса: {res[0]}\n'
             f'Пользователь: {res[1]}\n'
             f'<b>Описание проблемы:</b> {res[2]}\n'
             f'Исполняющий: {res[3]}\n'
             f'<u>Дата: {res[4]}</u>')

    await callback.message.edit_text(text=text, reply_markup=req_choice_interaction(res[0]))


@it_router.callback_query(F.data == 'admin_panel')
async def admin_panel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=emojize("⚠") + " Админ панель для избранных " + emojize("⚠"),
                                     reply_markup=admin_kb())


@it_router.callback_query(F.data == 'req_done')
async def req_done(callback: CallbackQuery):
    req_id = ''
    for i in range(34, len(callback.message.text)):
        if callback.message.text[i] == '\n':
            break

        req_id += callback.message.text[i]

    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"UPDATE users_requests SET status = 'done' WHERE req_id = {req_id}")

    connect.commit()
    cursor.close()
    connect.close()

    await callback.answer("Заявка отработана")
    await callback.message.answer(text=f'Заявка отработана {req_id}', reply_markup=return_butt())


@it_router.callback_query(F.data.startswith('appoint_task'))
async def appoint_task(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    kb = []
    cursor.execute('SELECT nickname FROM admins')
    for i in cursor.fetchall():
        kb.append([InlineKeyboardButton(text=i[0], callback_data=f"{i[0]} {callback.data[13:]}")])

    await callback.answer()
    await callback.message.edit_text(text='Выберите сотрудника', reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))


@it_router.callback_query(F.data[0] == '@')
async def app_emp(callback: CallbackQuery):
    await callback.answer()
    name = ''
    task_id = ''
    flag = False
    for i in callback.data:
        if flag:
            task_id += i
            continue

        if i == ' ':
            flag = True
            continue

        name += i

    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"UPDATE users_requests SET executive = '{name}' WHERE req_id = {task_id}")

    cursor.execute(f"SELECT id FROM admins WHERE nickname = '{name}'")
    admin_id = cursor.fetchone()

    cursor.execute("SELECT users_requests.req_id, users.username, users_requests.req_text, "
                   "users_requests.req_date FROM public.users_requests "
                   f"JOIN public.users ON users.user_id = users_requests.user_id WHERE req_id = {task_id}")
    res = cursor.fetchone()
    text = (f'ID запроса: {res[0]}\n'
            f'Пользователь: {res[1]}\n'
            f'<b>Описание проблемы:</b> {res[2]}\n'
            f'<u>Дата: {res[3]}</u>')

    connect.commit()
    cursor.close()
    connect.close()

    await callback.message.edit_text(text=f"Сотрудник назначен {name} на заявку {res[0]}", reply_markup=return_butt())
    await callback.bot.send_message(text='Вам назначена заявка\n' + text, chat_id=admin_id[0])
