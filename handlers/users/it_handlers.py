from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from utils.base_connect import conn
from keyboards.inline_kb import (req_choice_interaction, admin_kb, return_butt, kb_maker, take_task_kb,
                                 marks_or_invoices, mark_selected)
from emoji import emojize
from dotenv import load_dotenv
from os import getenv
from states.request_states import Marks

load_dotenv()
chat_id = getenv("CHAT_ID")
it_router = Router()

"""
Блок handler-ов общих запросов
"""


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
        await callback.message.edit_text(text=text, reply_markup=kb_maker(req_id, callback_char=''))

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


@it_router.callback_query(F.data.startswith("take_task"))
async def take_task(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"UPDATE users_requests SET executive = '@{callback.from_user.username}' "
                   f"WHERE req_id = {callback.data[10:]}")
    connect.commit()
    await callback.message.edit_text(text=f'Вам назначена заявка ID: {callback.data[10:]}', reply_markup=take_task_kb())
    await callback.answer()

    cursor.execute("SELECT users_requests.req_id, users.username, users_requests.req_text, "
                   "users_requests.executive, users_requests.req_date FROM public.users_requests "
                   f"JOIN public.users ON users.user_id = users_requests.user_id WHERE req_id = {callback.data[10:]}")
    res = cursor.fetchone()

    connect.commit()
    cursor.close()
    connect.close()

    text = (f'ID запроса: {res[0]}\n'
            f'Пользователь: {res[1]}\n'
            f'<b>Описание проблемы:</b> {res[2]}\n'
            f'Исполняющий: {res[3]}\n'
            f'<u>Дата: {res[4]}</u>')

    await callback.bot.send_message(text="<b><u>На заявку назначен исполняющий</u></b>\n" + text, chat_id=chat_id)


@it_router.callback_query(F.data == 'admin_panel')
async def admin_panel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=emojize("⚠") + " Админ панель для избранных " + emojize("⚠"),
                                     reply_markup=admin_kb())


@it_router.callback_query(F.data.startswith('req_done'))
async def req_done(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"UPDATE users_requests SET status = 'done' WHERE req_id = {callback.data[9:]}")
    cursor.execute(f"SELECT executive FROM users_requests WHERE req_id = {callback.data[9:]}")
    connect.commit()
    cursor.close()
    connect.close()

    await callback.answer("Заявка отработана")
    await callback.message.answer(text=f'Заявка отработана {callback.data[9:]}', reply_markup=return_butt())


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


"""
Блок обработки handler-ов по маркам
"""


@it_router.callback_query(F.data == 'marks_and_invoices')
async def marks_and_invoices(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text="Выберите действие", reply_markup=marks_or_invoices())


@it_router.callback_query(F.data == 'act_mark_req')
async def show_act_marks(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM marks_req WHERE done IS NULL")

    await callback.answer()

    if cursor.rowcount > 0:
        req_id = []
        text = '<u><b>Заявки по маркам</b></u>\n\n'
        for i in cursor.fetchall():
            req_id.append(i[0])
            text += (f'ID запроса: <b>{i[0]}</b>\n'
                     f'Имя пользователя: {i[2]}\n'
                     f'Наименование товара: {i[3]}\n'
                     f'Размер: {i[4]}\n'
                     f'Цвет: {i[5]}\n'
                     f'Количество: {i[6]}\n'
                     f'Причина: {i[7]}\n'
                     f'Дата: {i[8]}\n'
                     f'Комментарий: {i[10]}\n'
                     f'На модерации: {i[11]}\n\n')
        await callback.message.edit_text(text=text, reply_markup=kb_maker(req_id, '?'))


@it_router.callback_query(F.data.startswith('?'))
async def mark_select(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM marks_req WHERE req_id = {callback.data[1:]}")

    res = cursor.fetchone()

    text = (f'<u><b>Что сделать с запросом?</b></u>\n'
            f'ID запроса: <b>{res[0]}</b>\n'
            f'Имя пользователя: {res[2]}\n'
            f'Наименование товара: {res[3]}\n'
            f'Размер: {res[4]}\n'
            f'Цвет: {res[5]}\n'
            f'Количество: {res[6]}\n'
            f'Причина: {res[7]}\n'
            f'Дата: {res[8]}\n'
            f'Комментарий: {res[10]}\n'
            f'На модерации: {res[11]}')

    await callback.message.edit_text(text=text, reply_markup=mark_selected(req_id=res[0],
                                                                           access_date=res[11],
                                                                           done=res[9]))


@it_router.callback_query(F.data.startswith('in_moder'))
async def mark_access(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"UPDATE marks_req SET in_moderation = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' "
                   f"WHERE req_id = {callback.data[9:]}")

    connect.commit()
    cursor.close()
    connect.close()

    await callback.answer()
    await callback.message.edit_text(text="Данные обновлены", reply_markup=return_butt())


@it_router.callback_query(F.data.startswith('done'))
async def done(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"UPDATE marks_req SET done = 'true'"
                   f"WHERE req_id = {callback.data[5:]}")

    connect.commit()

    cursor.execute(f"SELECT * FROM marks_req WHERE req_id = {callback.data[5:]}")
    res = cursor.fetchone()

    connect.commit()
    cursor.close()
    connect.close()

    text = (f'ID запроса: <b>{res[0]}</b>\n'
            f'Имя пользователя: {res[2]}\n'
            f'Наименование товара: {res[3]}\n'
            f'Размер: {res[4]}\n'
            f'Цвет: {res[5]}\n'
            f'Количество: {res[6]}\n'
            f'Причина: {res[7]}\n'
            )

    await callback.answer()
    await callback.message.edit_text(text="Данные обновлены", reply_markup=return_butt())
    await callback.bot.send_message(chat_id=chat_id, text="<b><u>Можно забирать марки</u></b>\n" + text)
    await callback.bot.send_message(chat_id=chat_id, text="<b><u>Можно забирать марки</u></b>\n" + text)


@it_router.callback_query(F.data.startswith("collect"))
async def mark_collect(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"UPDATE marks_req SET user_collect = true WHERE req_id = {callback.data[8:]}")
    connect.commit()

    await callback.answer()
    await callback.message.answer(text=f"Заявка ID: {callback.data[8:]} закрыта", reply_markup=return_butt())


@it_router.callback_query(F.data.startswith('comment'))
async def comment_add(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Marks.add_comment)
    await state.update_data(req_id=callback.data[7:])
    await callback.answer()
    await callback.message.answer(text="Напишите комментарий")


@it_router.message(F.text, StateFilter(Marks.add_comment))
async def comment_push(message: Message, state: FSMContext):
    req_id = await state.get_data()
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"UPDATE marks_req SET comment = '{message.text}' WHERE req_id = {req_id['req_id']}")

    connect.commit()
    cursor.close()
    connect.close()

    await message.answer(text="Комментарий добавлен", reply_markup=return_butt())
    await state.set_state(None)


"""
Блок обработки handler-ов по накладным
"""


@it_router.callback_query(F.data == 'marks_and_invoices')
async def mark_or_invoice(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text="Выберите действие", reply_markup=marks_or_invoices())


@it_router.callback_query(F.data == 'act_invoices_req')
async def show_act_invoices(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM invoices_req WHERE can_do IS NULL")

    connect.commit()

    rows = cursor.fetchall()

    if cursor.rowcount > 0:
        req_id = []
        text = '<u><b>Заявки по накладным</b></u>\n\n'
        for res in rows:
            req_id.append(res[0])
            text += (f'ID запроса: <b>{res[0]}</b>\n'
                     f'Имя пользователя: {res[2]}\n'
                     f'Поставщик: {res[3]}\n'
                     f'Тип продукта: {res[4]}\n'
                     f'Дата приемки: {res[5]}\n'
                     f'Можно проводить: {res[6]}\n'
                     f'Дата принятия марок: {res[7]}\n'
                     f'Причина: {res[8]}\n\n')

        await callback.answer()
        await callback.message.answer(text=text, reply_markup=kb_maker(req_id=req_id, callback_char='^'))

    cursor.close()
    connect.close()


@it_router.callback_query(F.data.startswith('^'))
async def select_invoice(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM invoices_req WHERE req_id = {callback.data[1:]}")
    connect.commit()

    res = cursor.fetchone()
    cursor.close()
    connect.close()

    text = (f'<b><u>Что сделать с заявкой?</u></b>\n'
            f'ID запроса: <b>{res[0]}</b>\n'
            f'Имя пользователя: {res[2]}\n'
            f'Поставщик: {res[3]}\n'
            f'Тип продукта: {res[4]}\n'
            f'Дата приемки: {res[5]}\n'
            f'Можно проводить: {res[6]}\n'
            f'Дата принятия марок: {res[7]}\n'
            f'Причина: {res[8]}\n\n')

    await callback.answer()
    await callback.message.answer(text=text)


@it_router.callback_query(F.data.startswith("can_do"))
async def invoice_can_do(callback: CallbackQuery):
    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(f"UPDATE invoices_req SET can_do = true WHERE req_id = {callback.data[7:]}")
    connect.commit()

    cursor.close()
    connect.close()

    await callback.answer()
    await callback.message.answer()
