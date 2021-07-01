import re

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.callback_data import CallbackData
from keyboards.inline import *
from loader import bot, dp
from states import Mailing
from mailwizz_funcs import create_template, create_campaign
from misc.parse_funcs import TourSearch

city_from = None
tourists_num = None
country = None
dates_count = 0
dates = {dates_count: {'year': None, 'month': None, 'day': None}}
top_header = None
top_header_msg_id = None
bottom_header = None
bottom_header_msg_id = None
description = None
description_msg_id = None
image = None
image_msg_id = None
tourists_msg_id = None
from_to = None
duration = 7
link = None
price = None


def dates_list():
    global dates
    dates_ = []
    dates_string = ''
    if len(dates) == 0:
        return
    else:
        for k, v in dates.items():
            dates_.append(f'{v["day"]}.{v["month"]}.{v["year"]}')
    dates_string = '\n'.join(dates_)
    return dates_string

def create_link(nights, date, city, countryy):
    link = f'https://www.tez-tour.com/ru/kazan/search.html#result{{"priceMin":0,"priceMax":115000,"currency":"8390","nightsMin":{nights},"nightsMax":{nights},"hotelClassId":2568,"accommodationId":2,"rAndBId":15350,"tourType":"1","locale":"ru","cityId":{city},"countryId":"{countryy}","after":"{date}","before":"{date}","hotelInStop":false,"specialInStop":false,"version":2,"tourId":[[1285],[12689],[12706],[143330],[9004247],[70616],[4433],[45533],[5736],[139343],[4434],[12691],[21301],[12705],[4151426]],"hotelClassBetter":true,"rAndBBetter":true,"hotelId":[],"gdsHotelId":[],"noTicketsTo":false,"noTicketsFrom":false,"searchTypeId":3,"recommendedFlag":false,"salePrivateFlag":false,"onlineConfirmFlag":false,"promoFlag":true,"birthdays":"","contentCountryId":1102}}'
    return link

def create_tours():
    global country, duration, city_from
    tours = {}
    ts = TourSearch()
    ref = ts.get_reference()
    country_ref = ts.get_country_reference(ref['countries'][country])
    tid_str = ''
    tid_list = []
    for var in country_ref['tours'].values():
        tid_list = [var for var in TourSearch.get_country_reference(1104)['tours'].values()]
        tid_str = '&'.join(tid_list)
    for k, v in dates.items():
        date = f"{v['day']}.{v['month']}.{v['year']}"
        date_to = f"{v['day']}.{v['month']}"
        res, url = ts.find_tours(before=date, after=date, nightsMin=duration, nightsMax=duration, countryId=ref['countries'][country],
                             accomodationId=tourists_num, tourIds=tid_str, )
        hotels = ts.parse_results(res)
        price = int(hotels[k]['total']) // 2
        link = create_link(nights=duration, date=date, city=ref['cities'][city_from], countryy=ref['countries'][country])
        tours[k] = {'date_to': date_to, 'duration': duration, 'price': price, 'link': link}
    return tours


@dp.callback_query_handler(lambda query: query.data in ['email', 'ws'])
async def email(call: CallbackQuery, state: FSMContext):
    await Mailing.e_mail.set()
    await call.answer()
    await bot.edit_message_text(text='Выберите тип рассылки', chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.edit_message_reply_markup(call.from_user.id, reply_markup=choice_kb, message_id=call.message.message_id)


@dp.callback_query_handler(ml_cb.filter(type=['dates', 'hotels', 'info', 'back']), state=Mailing.e_mail)
async def choice(call: CallbackQuery, state: FSMContext):
    await call.answer()
    if call.data == 'mailing:dates':
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Собираем рассылку:\n\n'
                                    f'Город вылета: {city_from}\n'
                                    f'Кол-во туристов {tourists_num}\n'
                                    f'Страна: {country}\n'
                                    f'Даты вылета:\n {dates_list()}\n'
                                    f'Заголовок: {top_header}\n'
                                    f'Подзаголовок: {bottom_header}\n'
                                    f'Аннотация: {description}\n'
                                    f'Картинка в шапке (URL): {image}\n')
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=dates_kb)
        await Mailing.form_fill.set()

    if call.data == 'mailing:back':
        await bot.edit_message_text(text='Выберите тип рассылки', chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.edit_message_reply_markup(call.from_user.id, reply_markup=choice_kb, message_id=call.message.message_id)


@dp.callback_query_handler(lambda query: query.data in ['type:city_from', 'type:tourists_num', 'type:country', 'type:dates', 'type:top_header', 'type:bottom_header', 'type:description', 'type:image', 'type:test', 'type:send', 'type:duration'], state=Mailing.form_fill)
async def form_filling(call: CallbackQuery, state: FSMContext):
    global tourists_msg_id, top_header_msg_id, bottom_header_msg_id, description_msg_id, image_msg_id
    global city_from, tourists_num, country, dates, top_header, bottom_header, description, image, from_to, tours
    if call.data == 'type:city_from':
        await call.answer()
        await bot.edit_message_text(text='Выберите город вылета: ', chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=city_kb)
        await Mailing.city_choice.set()
    elif call.data == 'type:tourists_num':
        await call.answer()
        await bot.edit_message_text(text='Выберите кол-во туристов: ', chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=None)
        tourists_msg_id = call.message.message_id
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=tourists_num_pick)
        await Mailing.tourists_num.set()
    elif call.data == 'type:country':
        await call.answer()
        await bot.edit_message_text('Выберите страну: ', call.from_user.id, call.message.message_id)
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=country_kb)
        await Mailing.country_choice.set()
    elif call.data == 'type:dates':
        await call.answer()
        await bot.edit_message_text('Выберите параметр: ', call.from_user.id, call.message.message_id)
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=date_type_picker)
        await Mailing.date_type_pick.set()
    elif call.data == 'type:top_header':
        await call.answer()
        await bot.edit_message_text('Введите заголовок для рассылки: ', call.from_user.id, call.message.message_id, reply_markup=None)
        top_header_msg_id = call.message.message_id
        await Mailing.top_header.set()
    elif call.data == 'type:bottom_header':
        await call.answer()
        await bot.edit_message_text('Введите подзаголовок для рассылки: ', call.from_user.id, call.message.message_id, reply_markup=None)
        bottom_header_msg_id = call.message.message_id
        await Mailing.bottom_header.set()
    elif call.data == 'type:description':
        await call.answer()
        await bot.edit_message_text('Введите аннотацию (не более 300 знаков): ', call.from_user.id, call.message.message_id, reply_markup=None)
        description_msg_id = call.message.message_id
        await Mailing.description.set()
    elif call.data == 'type:image':
        await call.answer()
        await bot.edit_message_text('Введите URL картинки для рассылки: ', call.from_user.id, call.message.message_id, reply_markup=None)
        image_msg_id = call.message.message_id
        await Mailing.image_url.set()
    elif call.data == 'type:test':
        await call.answer(
            'Тестовая рассылка отправлена на почту kazan@tez-tour.com', show_alert=True)
        if city_from == 'Казань' and country == 'Турция':
            from_to = 'Анталия из Казани'
        if (country, image, top_header, tourists_num, dates, city_from) is not None:
            tours = create_tours()
            if len(tours) > 0:
                context = {'top_header': top_header, 'image_url': image,
                       'bottom_header': bottom_header, 'description': description,
                       'from_to': from_to, 'tours': create_tours()}
                template = create_template(context)
                create_campaign(subject=top_header, template=template)
    elif call.data == 'type:send':
        await call.answer(
            'Рассылка отправлена, статистика будет отправлена на kazan@tez-tour.com', show_alert=True)
    elif call.data == 'type:back':
        await call.answer()
        await bot.edit_message_text(text='Выберите тип рассылки', chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.edit_message_reply_markup(call.from_user.id, reply_markup=choice_kb, message_id=call.message.message_id)
        await state.reset_state()


@dp.callback_query_handler(lambda query: query.data in ['kazan', 'samara', 'moscow'], state=Mailing.city_choice)
async def city_choice(call: CallbackQuery, state: FSMContext):
    global city_from
    await call.answer()
    if call.data == 'kazan':
        city_from = 'Казань'
    elif call.data == 'moscow':
        city_from = 'Москва'
    elif call.data == 'samara':
        city_from = 'Самара'
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Собираем рассылку:\n\n'
                                f'Город вылета: {city_from}\n'
                                f'Кол-во туристов {tourists_num}\n'
                                f'Страна: {country}\n'
                                f'Даты вылета:\n {dates_list()}\n'
                                f'Заголовок: {top_header}\n'
                                f'Подзаголовок: {bottom_header}\n'
                                f'Аннотация: {description}\n'
                                f'Картинка в шапке (URL): {image}\n')
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=dates_kb)
    await Mailing.form_fill.set()


@dp.callback_query_handler(lambda query: query.data in ['Turkey'], state=Mailing.country_choice)
async def country_choice(call: CallbackQuery, state: FSMContext):
    global country
    await call.answer()
    if call.data == 'Turkey':
        country = "Турция"
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Собираем рассылку:\n\n'
                                f'Город вылета: {city_from}\n'
                                f'Кол-во туристов {tourists_num}\n'
                                f'Страна: {country}\n'
                                f'Даты вылета:\n {dates_list()}\n'
                                f'Заголовок: {top_header}\n'
                                f'Подзаголовок: {bottom_header}\n'
                                f'Аннотация: {description}\n'
                                f'Картинка в шапке (URL): {image}\n')
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=dates_kb)
    await Mailing.form_fill.set()

@dp.callback_query_handler(lambda query: query.data in ['dbl'], state=Mailing.tourists_num)
async def tourists_num_picker(call: CallbackQuery, state: FSMContext):
    global tourists_num
    await call.answer()
    if call.data == 'dbl':
        tourists_num = 2
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Собираем рассылку:\n\n'
                                f'Город вылета: {city_from}\n'
                                f'Кол-во туристов {tourists_num}\n'
                                f'Страна: {country}\n'
                                f'Даты вылета:\n {dates_list()}\n'
                                f'Заголовок: {top_header}\n'
                                f'Подзаголовок: {bottom_header}\n'
                                f'Аннотация: {description}\n'
                                f'Картинка в шапке (URL): {image}\n')
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=dates_kb)
    await Mailing.form_fill.set()


@dp.callback_query_handler(lambda query: query.data in ['year', 'month', 'day', 'back', 'done', 'more'], state=Mailing.date_type_pick)
async def date_type_pick(call: CallbackQuery, state: FSMContext):
    global dates, dates_count
    await call.answer()
    if call.data == 'year':
        await bot.edit_message_text(text='Выберите год', chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.edit_message_reply_markup(call.from_user.id, reply_markup=year_picker, message_id=call.message.message_id)
        await Mailing.year_pick.set()
    elif call.data == 'month':
        await bot.edit_message_text(text='Выберите месяц', chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.edit_message_reply_markup(call.from_user.id, reply_markup=month_picker, message_id=call.message.message_id)
        await Mailing.month_pick.set()
    elif call.data == 'day':
        await bot.edit_message_text(text='Выберите день', chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.edit_message_reply_markup(call.from_user.id, reply_markup=day_picker, message_id=call.message.message_id)
        await Mailing.day_pick.set()
    elif call.data == 'back':
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Собираем рассылку:\n\n'
                                    f'Город вылета: {city_from}\n'
                                    f'Кол-во туристов {tourists_num}\n'
                                    f'Страна: {country}\n'
                                    f'Даты вылета:\n {dates_list()}\n'
                                    f'Заголовок: {top_header}\n'
                                    f'Подзаголовок: {bottom_header}\n'
                                    f'Аннотация: {description}\n'
                                    f'Картинка в шапке (URL): {image}\n', reply_markup=dates_kb)
        await Mailing.form_fill.set()
    elif call.data == 'more':
        if len(dates) != 0:
            dates_count += 1
            dates[dates_count] = {'year': None, 'month': None, 'day': None}
        await bot.edit_message_text(f'Выбранные даты:\n {dates_list()}\n\nВыберите параметр: ', call.from_user.id, call.message.message_id)
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=date_type_picker)
        await Mailing.date_type_pick.set()
    elif call.data == 'done':
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Собираем рассылку:\n\n'
                                    f'Город вылета: {city_from}\n'
                                    f'Кол-во туристов {tourists_num}\n'
                                    f'Страна: {country}\n'
                                    f'Даты вылета:\n {dates_list()}\n'
                                    f'Заголовок: {top_header}\n'
                                    f'Подзаголовок: {bottom_header}\n'
                                    f'Аннотация: {description}\n'
                                    f'Картинка в шапке (URL): {image}\n', reply_markup=dates_kb)
        await Mailing.form_fill.set()


@dp.callback_query_handler(lambda query: query.data in [str(datetime.now().year)], state=Mailing.year_pick)
async def year_pick(call: CallbackQuery, state: FSMContext):
    global dates, dates_count
    await call.answer()
    dates[dates_count]['year'] = call.data
    await bot.edit_message_text(f'Выбранные даты:\n {dates_list()}\n\nВыберите параметр: ', call.from_user.id, call.message.message_id)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=date_type_picker)
    await Mailing.date_type_pick.set()


@dp.callback_query_handler(lambda query: query.data in [str(i) for i in range(1, 13, 1)], state=Mailing.month_pick)
async def month_pick(call: CallbackQuery, state: FSMContext):
    global dates, dates_count
    await call.answer()
    dates[dates_count]["month"] = str(0) + str(call.data)
    await bot.edit_message_text(f'Выбранные даты:\n {dates_list()}\n\nВыберите параметр: ', call.from_user.id, call.message.message_id)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=date_type_picker)
    await Mailing.date_type_pick.set()


@dp.callback_query_handler(lambda query: query.data in [str(i) for i in range(1, 32, 1)], state=Mailing.day_pick)
async def day_pick(call: CallbackQuery, state: FSMContext):
    global dates, dates_count
    await call.answer()
    dates[dates_count]['day'] = call.data
    await bot.edit_message_text(f'Выбранные даты:\n {dates_list()}\n\nВыберите параметр: ', call.from_user.id, call.message.message_id)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=date_type_picker)
    await Mailing.date_type_pick.set()


@dp.message_handler(state=Mailing.top_header)
async def top_header_pick(message: types.Message, state: FSMContext):
    global top_header
    err_msg: types.Message = None
    if not type(message.text) == str:
        err_msg = await bot.send_message(message.from_user.id, 'Пожалуйста, введите корректный заголовок')
    else:
        if err_msg is not None:
            await bot.delete_message(message.from_user.id, message_id=err_msg)
        top_header = message.text
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=top_header_msg_id,
                                text='Собираем рассылку:\n\n'
                                f'Город вылета: {city_from}\n'
                                f'Кол-во туристов {tourists_num}\n'
                                f'Страна: {country}\n'
                                f'Даты вылета:\n {dates_list()}\n\n'
                                f'Заголовок: {top_header}\n'
                                f'Подзаголовок: {bottom_header}\n'
                                f'Аннотация: {description}\n'
                                f'Картинка в шапке (URL): {image}\n', reply_markup=dates_kb)
    await Mailing.form_fill.set()


@dp.message_handler(state=Mailing.bottom_header)
async def top_header_pick(message: types.Message, state: FSMContext):
    global bottom_header
    err_msg: types.Message = None
    if not type(message.text) == str:
        err_msg = bot.send_message(
            message.from_user.id, 'Пожалуйста, введите корректный подзаголовок')
    else:
        bottom_header = message.text
        if err_msg is not None:
            await bot.delete_message(message.from_user.id, message_id=err_msg.message_id)
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=bottom_header_msg_id,
                                text='Собираем рассылку:\n\n'
                                f'Город вылета: {city_from}\n'
                                f'Кол-во туристов {tourists_num}\n'
                                f'Страна: {country}\n'
                                f'Даты вылета:\n {dates_list()}\n'
                                f'Заголовок: {top_header}\n'
                                f'Подзаголовок: {bottom_header}\n'
                                f'Аннотация: {description}\n'
                                f'Картинка в шапке (URL): {image}\n', reply_markup=dates_kb)
    await Mailing.form_fill.set()


@dp.message_handler(state=Mailing.description)
async def top_header_pick(message: types.Message, state: FSMContext):
    global description
    err_msg: types.Message = None
    err_msg1: types.Message = None
    if len(message.text) > 200:
        err_msg1 = await bot.send_message(message.from_user.id, 'Длина сообщения превышена')
    else:
        description = message.text
        if err_msg is not None:
            await bot.delete_message(message.from_user.id, message_id=err_msg.message_id)
        elif err_msg1 is not None:
            await bot.delete_message(message.from_user.id, message_id=err_msg1.message_id)
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=description_msg_id,
                                text='Собираем рассылку:\n\n'
                                f'Город вылета: {city_from}\n'
                                f'Кол-во туристов {tourists_num}\n'
                                f'Страна: {country}\n'
                                f'Даты вылета:\n {dates_list()}\n'
                                f'Заголовок: {top_header}\n'
                                f'Подзаголовок: {bottom_header}\n'
                                f'Аннотация: {description}\n'
                                f'Картинка в шапке (URL): {image}\n', reply_markup=dates_kb)
    await Mailing.form_fill.set()


@dp.message_handler(state=Mailing.image_url)
async def top_header_pick(message: types.Message, state: FSMContext):
    global image
    err_msg: types.Message = None
    if not (message.text).lower().startswith('http'):
        err_msg = await bot.send_message(message.from_user.id, 'Пожалуйста, введите корректный URL')
    else:
        image = message.text
        if err_msg is not None:
            await bot.delete_message(message.from_user.id, message_id=err_msg.message_id)
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=image_msg_id,
                                text='Собираем рассылку:\n\n'
                                f'Город вылета: {city_from}\n'
                                f'Кол-во туристов {tourists_num}\n'
                                f'Страна: {country}\n'
                                f'Даты вылета:\n {dates_list()}\n'
                                f'Заголовок: {top_header}\n'
                                f'Подзаголовок: {bottom_header}\n'
                                f'Аннотация: {description}\n'
                                f'Картинка в шапке (URL): {image}\n', reply_markup=dates_kb)
    await Mailing.form_fill.set()
