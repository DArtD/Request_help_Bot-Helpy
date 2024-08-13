from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from emoji import emojize
from TBot import admins


def ease_link_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Мой хабр", url='https://habr.com/ru/users/yakvenalex/')],
        [InlineKeyboardButton(text="Мой Telegram", url='tg://resolve?domain=yakvenalexx')],
        [InlineKeyboardButton(text="Веб приложение", web_app=WebAppInfo(url="https://tg-promo-bot.ru/questions"))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def req_kb(user_id: int):
    inline_kb_list = [
        [InlineKeyboardButton(text='Отправить заявку ' + emojize(':envelope:'), callback_data='req_send')],
        [InlineKeyboardButton(text='Отправленные заявки ' + emojize(':closed_book:'), callback_data='my_req')],
    ]

    if user_id == int(admins):
        inline_kb_list.append([InlineKeyboardButton(text='Админ панель ' + emojize(":hammer_and_wrench:"),
                                                    callback_data='admin_panel')])
        inline_kb_list.append([InlineKeyboardButton(text='Активные заявки ', callback_data='active_req')])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def my_req_kb(reqs_date: list):
    inline_kb_list = []
    for i in reqs_date:
        inline_kb_list.append([InlineKeyboardButton(text=f'Заявка от {i}')])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def cancel_butt():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='<< Отмена', callback_data='cancel')]])


def return_butt():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='<< Вернуться', callback_data='cancel')]])


def accept_butt():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Выбрать >>', callback_data='accept')]])


def req_choice_interaction():
    kb = [[InlineKeyboardButton(text='Закрыть заявку', callback_data='cancel')],
          [InlineKeyboardButton(text='Связаться с пользователем', callback_data='cancel')],
          [InlineKeyboardButton(text='<< Вернуться', callback_data='cancel')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def admin_kb():
    kb = [[InlineKeyboardButton(text='Назначить заявки', callback_data='appoint_task')],
          [InlineKeyboardButton(text='Создать документ активности сотрудников', callback_data='doc_create')],
          [InlineKeyboardButton(text='Добавить админа', callback_data='admin_add')],
          [InlineKeyboardButton(text='<< Вернуться', callback_data='cancel')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)
