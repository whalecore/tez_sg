from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from loader import dp
from keyboards.inline import ws_em_kb


@dp.message_handler(CommandStart())
async def start_cmd(message: types.Message):
    bot = dp.bot
    kb = ws_em_kb
    await bot.send_message(message.from_user.id, 'Создание и отправка рассылок по e-mail и WhatsApp.', reply_markup=ws_em_kb)
