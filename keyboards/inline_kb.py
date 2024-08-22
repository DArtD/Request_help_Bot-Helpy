from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from TBot import admins


def req_kb(user_id: int):
    inline_kb_list = [
        # [InlineKeyboardButton(text='Отправить заявку ' + emojize('✉'), callback_data='req_send')],
        # [InlineKeyboardButton(text='Отправленные заявки ' + emojize('📕'), callback_data='my_req')],
        [InlineKeyboardButton(text='Заказать марку ' + emojize('🔖'), callback_data='marks')],
        [InlineKeyboardButton(text='Накладные ' + emojize('📑'), callback_data='invoice')],
    ]

    if user_id == int(admins):
        inline_kb_list.append([InlineKeyboardButton(text='Админ панель ' + emojize("🛠"),
                                                    callback_data='admin_panel')])

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
    kb = [[InlineKeyboardButton(text='Закрыть заявку ' + emojize("✅"), callback_data=f'user_question {req_id}')],
          [InlineKeyboardButton(text='Назначить исполняющего ', callback_data=f'appoint_task {req_id}')],
          [InlineKeyboardButton(text='Взять заявку ', callback_data=f'take_task {req_id}')],
          [InlineKeyboardButton(text=emojize('🔙 ') + ' Обратно к списку ', callback_data='active_req')],
          [InlineKeyboardButton(text=emojize('🔙 ') + ' Вернуться', callback_data='cancel')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def take_task_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=emojize('🔙 ') + ' К списку задач ', callback_data='my_active_req')],
                         [InlineKeyboardButton(text=emojize('🔙 ') + ' Вернуться', callback_data='cancel')]])


def admin_kb():
    kb = [[InlineKeyboardButton(text='Активные заявки ' + emojize('⚙'), callback_data='active_req')],
          [InlineKeyboardButton(text='Создать документ активности сотрудников ' + emojize('📊'),
                                callback_data='doc_create')],
          [InlineKeyboardButton(text='Добавить админа ' + emojize('➕👨‍💼'), callback_data='admin_add')],
          [InlineKeyboardButton(text='Марки и накладные ' + emojize('🔖📑'), callback_data='marks_and_invoices')],
          [InlineKeyboardButton(text=emojize('🔙 ') + ' Вернуться', callback_data='cancel')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def kb_maker(req_id: list, callback_char: str):
    col_count = 0
    kb = []
    row = []
    for i in req_id:
        row.append(InlineKeyboardButton(text=f'ID: {i}', callback_data=callback_char + str(i)))
        col_count += 1

        if col_count == 5:
            kb.extend([row])
            row = []
            col_count = 0
    else:
        if 0 < col_count < 5:
            kb.extend([row])

    kb.append([InlineKeyboardButton(text=emojize('🔙 ') + ' Вернуться', callback_data='cancel')])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def user_req(req_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Отменить заявку', callback_data=f'//{req_id}')],
                         [InlineKeyboardButton(text=emojize('🔙 ') + ' Вернуться',
                                               callback_data='cancel')]])


def yes_no_kb(req_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Да', callback_data=f'req_done {req_id}')],
                         [InlineKeyboardButton(text='Нет', callback_data='no')]])


def marks_or_invoices():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Активные заявки на марки' + emojize('🔖'),
                                               callback_data='act_mark_req')],
                         [InlineKeyboardButton(text='Активные заявки на накладные' + emojize('📑'),
                                               callback_data='act_invoices_req')],
                         [InlineKeyboardButton(text=emojize('🔙 ') + 'Вернуться',
                                               callback_data='cancel')]])


def mark_selected(req_id, access_date=None, done=None):
    kb = []
    if access_date is None:
        kb.append([InlineKeyboardButton(text='На модерации ' + emojize('⚙'), callback_data=f"in_moder {req_id}")])

    elif done is None:
        kb.append([InlineKeyboardButton(text='Можно забирать', callback_data=f"done {req_id}")])

    else:
        kb.append([InlineKeyboardButton(text='Марку забрали', callback_data=f"collect {req_id}")])

    kb.append([InlineKeyboardButton(text='Добавить коммент', callback_data=f'comment {req_id}')])
    kb.append([InlineKeyboardButton(text='Отмена', callback_data='act_mark_req')])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def invoice_selected(req_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Можно проводить " + emojize('✅'),
                                               callback_data='can_do' + req_id)],
                         [InlineKeyboardButton(text='Нельзя проводить ' + emojize('🚫'),
                                               callback_data='not_can_do' + req_id)],
                         [InlineKeyboardButton(text='Добавить дату принятия марок ' + emojize('📆'),
                                               callback_data='add_access_date' + req_id)],
                         [InlineKeyboardButton(text=emojize('🔙 ') + ' Вернуться', callback_data='act_invoices_req')]])
