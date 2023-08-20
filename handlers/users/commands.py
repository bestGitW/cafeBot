from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hitalic, hunderline, hstrikethrough, hlink

from keyboards import commands_keyboard
from loader import dp, db


@dp.message_handler(text=['Привет', 'Начать'])
@dp.message_handler(commands='start')
async def answer_start_command(message: types.Message):
    await message.answer(text=f'Привет, {hbold(message.from_user.username)}!'
                              f'\nРад тебя видеть!'
                              f'\nЯ - {hitalic("ОВОЩЕ_БОТ")} {hstrikethrough("ТЕРМИНАТОР")}😸'
                              f'\nБудем вместе делать {hunderline("покупки")}🥦'
                              f'\nА это мой создатель, пиши ему, если что: {hlink(url=r"https://t.me/tochno_slava", title="тык")}',
                         reply_markup=commands_keyboard)


@dp.message_handler(text=['Помощь'])
@dp.message_handler(commands=['help'])
async def answer_help_command(message: types.Message):
    await message.answer(text='/start - приветствие'
                              '\n/item - ассортимент'
                              '\n/help - доступные команды')


@dp.message_handler(text=['О нас'])
@dp.message_handler(commands=['info'])
async def answer_info_command(message: types.Message):
    await message.answer(text='Мы - интернет магазин!')


@dp.message_handler(commands=['menu'])
async def answer_menu_command(message: types.Message):
    await message.answer(text='Главное меню.',
                         reply_markup=commands_keyboard)


@dp.message_handler(text=['Скрыть меню'])
async def answer_close_command(message: types.Message):
    await message.answer(text='Чтобы вернуть меню, воспользуйтесь командой /menu',
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=['contact'])
async def answer_contact_command(message: types.Message):
    if message.contact.user_id == message.from_user.id:
        await message.answer(text='Регистрация прошла успешно!')
        db.add_user(int(message.from_user.id), str(message.contact.phone_number))
    else:
        await message.answer(text='Увы(')
