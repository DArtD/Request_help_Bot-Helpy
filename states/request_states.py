from aiogram.fsm.state import StatesGroup, State


class RequestCreation(StatesGroup):
    req_waiting = State()
    address = State()
    St3 = State()
