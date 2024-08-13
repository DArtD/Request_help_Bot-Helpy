from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboards.inline_kb import req_kb

start_router = Router()


@start_router.callback_query(F.data == "cancel")
async def start_cmd(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text="Я - бот помощник для оправки заявок IT-отделу",
                                     reply_markup=req_kb(callback.from_user.id))


@start_router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(text="Я - бот помощник для оправки заявок IT-отделу",
                         reply_markup=req_kb(message.from_user.id))


# @start_router.message(F.text == 'Давай инлайн!')
# async def get_inline_btn_link(message: Message):
#     await message.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=ease_link_kb())


@start_router.message(Command("id"))  # Хендлер команды /id. Определяет id чата
async def chat_id(message: Message):
    await message.answer(f"ID чата: {message.chat.id}")
