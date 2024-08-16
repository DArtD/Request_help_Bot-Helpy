from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from TBot import admins


def req_kb(user_id: int):
    inline_kb_list = [
        [InlineKeyboardButton(text='Отправить заявку ' + emojize('✉'), callback_data='req_send')],
        [InlineKeyboardButton(text='Отправленные заявки ' + emojize('📕'), callback_data='my_req')],
    ]

    if user_id == int(admins):
        inline_kb_list.append([InlineKeyboardButton(text='Админ панель ' + emojize("🛠"),
                                                    callback_data='admin_panel')])
        inline_kb_list.append([InlineKeyboardButton(text='Активные заявки ' + emojize('⚙'),
                                                    callback_data='active_req')])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def cancel_butt():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=emojize('🔙 ') + 'Отмена',
                                                                       callback_data='cancel')]])


def return_butt():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=emojize('🔙 ') + ' Вернуться',
                                                                       callback_data='cancel')]])


def req_sender():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отправленные заявки ' + emojize('📕'),
                                                                       callback_data='my_req')],
                                                 [InlineKeyboardButton(text=emojize('🔙 ') + ' Вернуться',
                                                                       callback_data='cancel')]])


def accept_butt():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Выбрать ' + emojize('🔜 '),
                                                                       callback_data='accept')]])


def req_choice_interaction(req_id):
    kb = [[InlineKeyboardButton(text='Закрыть заявку ' + emojize("✅"), callback_data='req_done')],
          [InlineKeyboardButton(text='Связаться с пользователем ' + emojize("💼"), callback_data='cancel')],
          [InlineKeyboardButton(text='Назначить исполняющего ', callback_data=f'appoint_task {req_id}')],
          [InlineKeyboardButton(text='Взять заявку ', callback_data='cancel')],
          [InlineKeyboardButton(text=emojize('🔙 ') + ' Обратно к списку ', callback_data='active_req')],
          [InlineKeyboardButton(text=emojize('🔙 ') + ' Вернуться', callback_data='cancel')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def admin_kb():
    kb = [[InlineKeyboardButton(text='Назначить заявки ' + emojize('🗂'), callback_data='appoint_task')],
          [InlineKeyboardButton(text='Создать документ активности сотрудников ' + emojize('📊'),
                                callback_data='doc_create')],
          [InlineKeyboardButton(text='Добавить админа ' + emojize('➕👨‍💼'), callback_data='admin_add')],
          [InlineKeyboardButton(text=emojize('🔙 ') + ' Вернуться', callback_data='cancel')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def kb_maker(req_id: list):
    col_count = 0
    kb = []
    row = []
    for i in req_id:
        row.append(InlineKeyboardButton(text=f'ID: {i}', callback_data=str(i)))
        col_count += 1

        if col_count == 5:
            kb.extend([row])
            row = []
            col_count = 0
    else:
        if 1 < col_count < 5:
            kb.extend([row])

    kb.append([InlineKeyboardButton(text=emojize('🔙 ') + ' Вернуться', callback_data='cancel')])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def kb_maker_users(req_id: list):
    col_count = 0
    kb = []
    row = []
    for i in req_id:
        row.append(InlineKeyboardButton(text=f'ID: {i}', callback_data='!' + str(i)))
        col_count += 1

        if col_count == 5:
            kb.extend([row])
            row = []
            col_count = 0
    else:
        if 1 < col_count < 5:
            kb.extend([row])

    kb.append([InlineKeyboardButton(text=emojize('🔙 ') + ' Вернуться', callback_data='cancel')])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def user_req(req_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Отменить заявку', callback_data=f'//{req_id}')],
                         [InlineKeyboardButton(text=emojize('🔙 ') + ' Вернуться',
                                               callback_data='cancel')]])
