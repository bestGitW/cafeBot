from aiogram import types
from aiogram.types import ContentType

from keyboards import commands_keyboard
from loader import dp, bot
from config import upay_token


@dp.message_handler(commands=['money'])
async def add_money(message: types.Message):
    await bot.send_invoice(chat_id=message.from_user.id,
                           title="Пополнение баланса!",
                           description=f'Пополнение баланса на 100₽',
                           payload='add_money_100',
                           provider_token=upay_token,
                           currency="RUB",
                           start_parameter='add_money_100',
                           prices=[{
                               "label": "Rub",
                               "amount": 10000
                           }])


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "add_money_100":
        ###
        # Пополняем счет в бд
        ###
        await message.answer(text=f"Операция выполнена успешно!",
                             reply_markup=commands_keyboard)