from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message, CallbackQuery
from keyboards.inline_kb import req_kb
from TBot import dp

start_router = Router()


@start_router.callback_query(F.data == "cancel")
async def start_cmd(callback: CallbackQuery):
    state = FSMContext(storage=dp.storage, key=StorageKey(chat_id=callback.from_user.id,
                                                          user_id=callback.from_user.id,
                                                          bot_id=callback.bot.id))

    await state.set_state(None)
    await callback.answer()
    await callback.message.edit_text(text="Я - бот помощник для оправки заявок IT-отделу",
                                     reply_markup=req_kb(callback.from_user.id))


@start_router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(text="Я - бот помощник для оправки заявок IT-отделу",
                         reply_markup=req_kb(message.from_user.id))


@start_router.message(Command("id"))  # Хендлер команды /id. Определяет id чата
async def chat_id(message: Message):
    await message.answer(f"ID чата: {message.chat.id}")
