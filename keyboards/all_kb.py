from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from TBot import admins


def main_kb(user_id: int):
    kb_list = [
        [KeyboardButton(text="Отправить заявку"), KeyboardButton(text="Мои заявки")]
    ]

    if user_id == int(admins):
        kb_list.append([KeyboardButton(text='Админ панель')])

    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True,
                                   one_time_keyboard=True, input_field_placeholder="Выберите действие")
    return keyboard
