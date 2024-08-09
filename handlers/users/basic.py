from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from filters.Users import Users


router = Router()


@router.message(CommandStart(), Users())
async def start_cmd(message: Message):
    await message.answer("Я - бот помощник для оправки заявок IT-отделу")


@router.message(Command("id"))
async def chat_id(message: Message):
    await message.answer(f"ID чата: {message.chat.id}")