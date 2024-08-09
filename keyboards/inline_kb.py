from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


def ease_link_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Мой хабр", url='https://habr.com/ru/users/yakvenalex/')],
        [InlineKeyboardButton(text="Мой Telegram", url='tg://resolve?domain=yakvenalexx')],
        [InlineKeyboardButton(text="Веб приложение", web_app=WebAppInfo(url="https://tg-promo-bot.ru/questions"))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def req_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text='Отправить заявку', callback_data='req_send')],
        [InlineKeyboardButton(text='Отправленные заявки', callback_data='my_req')],
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def my_req_kb(reqs_date: list):
    inline_kb_list = []
    for i in reqs_date:
        inline_kb_list.append([InlineKeyboardButton(text=f'Заявка от {i}')])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def cancel_butt():
    return InlineKeyboardButton(text='Отмена', callback_data='cancel')
