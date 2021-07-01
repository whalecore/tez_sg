from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

class AccessMiddleware(BaseMiddleware):
    def __init__(self, admin_id):
        self.admin_id = admin_id
        super().__init__()

    async def on_proccess_message(self, message: types.Message, _):
        if int(message.from_user.id) != int(self.admin_id):
            await message.answer("Нет доступа")
            raise CancelHandler()