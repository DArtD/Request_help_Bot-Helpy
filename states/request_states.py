from aiogram.fsm.state import StatesGroup, State


class RequestCreation(StatesGroup):
    req_waiting = State()   # состояние ожидания запроса от пользователя
    address = State()
    St3 = State()
