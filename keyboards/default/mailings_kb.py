from aiogram import types

mailings_kb = types.ReplyKeyboardMarkup(keyboard=[
    [
        types.KeyboardButton('E-mail')
    ],
    [
        types.KeyboardButton('WhatsApp')
    ]
],
    resize_keyboard=True, one_time_keyboard=True)

# mailings_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
# btn1 = types.KeyboardButton('E-mail')
# btn2 = types.KeyboardButton('WhatsApp')
# mailings_kb.add(btn1, btn2)

# email_kb = types.ReplyKeyboardMarkup(keyboard=[
#     [types.KeyboardButton('По датам')],
#     [types.KeyboardButton('По отелям')],
#     [types.KeyboardButton('Информация')],
#     [types.KeyboardButton('Назад')]
# ],
#     resize_keyboard=True, one_time_keyboard=False)

# whatsapp_kb = types.ReplyKeyboardMarkup([
#     [types.KeyboardButton('По датам')],
#     [types.KeyboardButton('По отелям')],
#     [types.KeyboardButton('Информация')],
#     [types.KeyboardButton('Назад')]

# # ],
# #     resize_keyboard=True, one_time_keyboard=False)
