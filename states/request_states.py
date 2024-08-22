from aiogram.fsm.state import StatesGroup, State


class RequestCreation(StatesGroup):
    req_waiting = State()   # состояние ожидания запроса от пользователя
    address = State()
    St3 = State()


class RequestEnd(StatesGroup):
    accept_wait = State()


class Marks(StatesGroup):
    mark_name = State()
    size = State()
    color = State()
    quantity = State()
    reason = State()
    add_comment = State()


class Invoices(StatesGroup):
    provider = State()
    invoice_num = State()
    prod_type = State()

