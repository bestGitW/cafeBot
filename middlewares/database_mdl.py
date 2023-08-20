from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import db


class GetDBUser(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        data['user_basket'] = db.select_user_basket(id=message.from_user.id)
        data['some_data'] = 'INFO'

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        data['info'] = 'some_info'
