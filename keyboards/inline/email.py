import calendar
from datetime import datetime
from aiogram import types
from aiogram.utils.callback_data import CallbackData

ml_cb = CallbackData('mailing', 'type')
dates_cb = CallbackData('type', 'data')

ws_em_kb = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [types.InlineKeyboardButton(text='E-mail', callback_data='email'),
    types.InlineKeyboardButton(text='WhatsApp', callback_data='ws')],
])

dates_kb = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [types.InlineKeyboardButton(
        text='Откуда', callback_data=dates_cb.new(data='city_from')),
    types.InlineKeyboardButton(
        text='Кол-во туристов', callback_data=dates_cb.new(data='tourists_num'))],
    [types.InlineKeyboardButton(text='Длительность', callback_data=dates_cb.new(data='duration'))],
    [types.InlineKeyboardButton(
        text='Страна', callback_data=dates_cb.new(data='country')),
    types.InlineKeyboardButton(
        text='Даты', callback_data=dates_cb.new(data='dates'))],
    [types.InlineKeyboardButton(
        text='Заголовок', callback_data=dates_cb.new(data='top_header')),
    types.InlineKeyboardButton(
        text='Подзаголовок', callback_data=dates_cb.new(data='bottom_header'))],
    [types.InlineKeyboardButton(
        text='Аннотация', callback_data=dates_cb.new(data='description')),
    types.InlineKeyboardButton(
        text='Картинка', callback_data=dates_cb.new(data='image'))],
    [types.InlineKeyboardButton(
        text='Тест', callback_data=dates_cb.new(data='test')),
    types.InlineKeyboardButton(
        text='Отправка', callback_data=dates_cb.new(data='send'))],
    [types.InlineKeyboardButton(
        text='Назад', callback_data=dates_cb.new(data='back'))]
])

choice_kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(
        text='По датам', callback_data=ml_cb.new(type='dates')),
    types.InlineKeyboardButton(
        text='По отелям', callback_data=ml_cb.new(type='hotels'))],
    [types.InlineKeyboardButton(
        text='Инфо', callback_data=ml_cb.new(type='info')),
    types.InlineKeyboardButton(
        text='Назад', callback_data=ml_cb.new(type='back'))]
])

city_kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Казань", callback_data='kazan')],
    [types.InlineKeyboardButton(text="Москва", callback_data='moscow')],
    [types.InlineKeyboardButton(text="Самара", callback_data='samara')],
])

country_kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Турция", callback_data='Turkey')],
])

date_type_picker = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [types.InlineKeyboardButton(text="Год", callback_data='year'),
    types.InlineKeyboardButton(text="Месяц", callback_data='month'),
    types.InlineKeyboardButton(text='День', callback_data='day')],
    [types.InlineKeyboardButton(text='Добавить', callback_data='more')],
    [types.InlineKeyboardButton(text='Готово', callback_data='done'),
        types.InlineKeyboardButton(text='Назад', callback_data='back')],
])

year_picker = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(
        text=str(datetime.now().year), callback_data=str(datetime.now().year))],

])

this_month = datetime.now().month
this_year = datetime.now().year
cal = calendar.Calendar()


def get_days():
    days = []
    for i in cal.itermonthdays(this_year, this_month):
        if i != 0:
            days.append(i)
    return days


month_picker = types.InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [types.InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 4, 1)],
    [types.InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(4, 7, 1)],
    [types.InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(7, 10, 1)],
    [types.InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(10, 13, 1)]
])

day_picker= types.InlineKeyboardMarkup(row_width=7, inline_keyboard=[
    [types.InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in cal.itermonthdays(this_year, this_month) if i != 0 and i < 8],
    [types.InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in cal.itermonthdays(this_year, this_month) if i != 0 and 15 > i > 8],
    [types.InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in cal.itermonthdays(this_year, this_month) if i != 0 and 22 > i > 15],
    [types.InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in cal.itermonthdays(this_year, this_month) if i != 0 and 29 > i > 22],
    [types.InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in cal.itermonthdays(this_year, this_month) if i != 0 and i > 28],
])

date_more = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [types.InlineKeyboardButton(text='Да', callback_data='yes'),
    types.InlineKeyboardButton(text='Нет', callback_data='no')
    ]
])

date_more = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [types.InlineKeyboardButton(text='Да', callback_data='yes'),
    types.InlineKeyboardButton(text='Нет', callback_data='no')
    ]
])

tourists_num_pick = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [types.InlineKeyboardButton(text='DBL', callback_data='dbl')]
])