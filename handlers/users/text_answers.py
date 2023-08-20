from loader import dp
from aiogram import types


@dp.message_handler(text=['Редиска','редиска'])
async def answer_start_command(message: types.Message):
    await message.answer(text=f"Не хорошо ругаться")

@dp.message_handler(text=['Огурец', 'Помидор','огурец', 'помидор'])
async def answer_start_command(message: types.Message):
    await message.answer(text=f"Салат сделать хочешь?")