from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from utils.base_connect import conn
from utils.str_check import str_check, str_check_for_nums
from datetime import datetime
from os import getenv
from dotenv import load_dotenv
from states.request_states import Marks, Invoices
from keyboards.inline_kb import return_butt

load_dotenv()
warehouse = Router()
lilya_id = getenv("LILYA")
admin_id = getenv('ADMINS')
chars = set('0123456789* ')

"""
Блок пользовательских handler-ов для выпуска новых марок 
"""


@warehouse.callback_query(F.data == 'marks')
async def marks(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Marks.mark_name)
    await callback.message.answer("Напишите наименование товара")


@warehouse.message(F.text, StateFilter(Marks.mark_name))
async def mark_size(message: Message, state: FSMContext):
    await state.update_data(mark_name=message.text)
    await state.set_state(Marks.size)
    await message.answer("Напишите размер товара")


@warehouse.message(F.text, StateFilter(Marks.size))
async def mark_color(message: Message, state: FSMContext):
    if await str_check_for_nums(message.text, set('123456789* ')):
        await state.update_data(mark_size=message.text)
        await state.set_state(Marks.color)
        await message.answer("Введите цвет товара")

    else:
        await message.answer("Ошибка ввода размера\n"
                             "Используйте 1 из способов ввода\n"
                             "Пример размера одежды: 46\n"
                             "Пример размера объемных товаров: 100*80")


@warehouse.message(F.text, StateFilter(Marks.color))
async def mark_quantity(message: Message, state: FSMContext):
    if await str_check(message.text, set('123456789')):
        await state.update_data(mark_color=message.text)
        await state.set_state(Marks.quantity)
        await message.answer("Введите количество марок")

    else:
        await message.answer("Ошибка ввода цвета\n"
                             "(цвет не может состоять из цифр)")


@warehouse.message(F.text, StateFilter(Marks.quantity))
async def reason(message: Message, state: FSMContext):
    if await str_check_for_nums(message.text, set('123456789')):
        await state.update_data(mark_quantity=message.text)
        await state.set_state(Marks.reason)
        await message.answer("Опишите причину заказа новой марки")

    else:
        await message.answer("Ошибка ввода количества марок\n"
                             "Введите цифру или число")


@warehouse.message(F.text, StateFilter(Marks.reason))
async def ending(message: Message, state: FSMContext):
    await state.update_data(reason=message.text)
    data = await state.get_data()

    connect = await conn()
    cursor = connect.cursor()
    cursor.execute(
        "INSERT INTO marks_req (user_id, username, prod_name, prod_size, prod_color, prod_quantity, user_reason, "
        "req_date)"
        f"VALUES ({message.from_user.id}, '@{message.from_user.username}', '{data['mark_name']}', "
        f"'{data['mark_size']}', '{data['mark_color']}',"
        f" {data['mark_quantity']}, '{data['reason']}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')")

    connect.commit()
    cursor.close()
    connect.close()

    text = (f"<b><u>Запрос по маркам</u></b>\n"
            f"Пользователь: @{message.from_user.username}\n"
            f"Наименование марки: {data['mark_name']}\n"
            f"Размер: {data['mark_size']}\n"
            f"Цвет: {data['mark_color']}\n"
            f"Количество: {data['mark_quantity']}\n"
            f"Причина: {data['reason']}\n")
    await message.bot.send_message(chat_id=admin_id, text=text)
    await message.answer("Запрос направлен: @liliya_orsk\nКогда марки будут готовы, вас уведомят",
                         reply_markup=return_butt())
    await state.set_state(None)


"""
Блок пользовательских handler-ов для запросов приемки
"""


@warehouse.callback_query(F.data == "invoice")
async def provider_input(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите поставщика')
    await state.set_state(Invoices.provider)


@warehouse.message(F.text, StateFilter(Invoices.provider))
async def provider_input(message: Message, state: FSMContext):
    await state.update_data(provider=message.text)
    await message.answer('Введите номер накладной')
    await state.set_state(Invoices.invoice_num)


@warehouse.message(F.text, StateFilter(Invoices.invoice_num))
async def prod_type_input(message: Message, state: FSMContext):
    if await str_check_for_nums(message.text, set('123456789')):
        await state.update_data(invoice_num=message.text)
        await message.answer("Введите тип товара")
        await state.set_state(Invoices.prod_type)

    else:
        await message.answer("Ошибка ввода номера накладной\n"
                             "Используйте только цифры")


@warehouse.message(F.text, StateFilter(Invoices.prod_type))
async def invoice_req(message: Message, state: FSMContext):
    if await str_check(message.text, set('123456789')):
        await state.update_data(prod_type=message.text)
        data = await state.get_data()

        connect = await conn()
        cursor = connect.cursor()
        cursor.execute("INSERT INTO invoices_req (user_id, username, provider, prod_type, access_date) "
                       f"VALUES ({message.from_user.id}, '@{message.from_user.username}', '{data['provider']}', "
                       f"'{data['prod_type']}', '{datetime.now().strftime('%Y-%m-%d')}')")

        connect.commit()
        cursor.close()
        connect.close()

        text = (f"<u><b>Запрос по накладным</b></u>\n"
                f"Пользователь: @{message.from_user.username}\n"
                f"Поставщик: {data['provider']}\n"
                f"Номер накладной: {data['invoice_num']}\n"
                f"Тип товара: {data['prod_type']}\n"
                f"Дата приемки: {datetime.now().strftime('%Y-%m-%d')}\n")

        await message.bot.send_message(chat_id=admin_id, text=text)
        await message.answer(text="Запрос направлен: @liliya_orsk\nКогда все будет готово, вас уведомят",
                             reply_markup=return_butt())

    else:
        await message.answer("Ошибка ввода типа товара\n"
                             "Введите тип товара без цифр")
