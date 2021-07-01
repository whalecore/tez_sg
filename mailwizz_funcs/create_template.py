from jinja2 import Template

html = open('mailwizz_funcs/dates_template.html', 'r', encoding='utf-8').read()
template = Template(html)

top_header = 'Тестовый шаблон'
image_url = 'https://jinja.palletsprojects.com/en/2.11.x/_static/jinja-logo-sidebar.png'
bottom_header = 'Уважаемые коллеги!'
description = 'Я тестирую шаблон'
from_to = 'Анталия из Казани'
tours = {
    1: {'date_to': '28.04', 'duration': 7, 'link': 'https://plus.tez-tour.com', 'price': '20 000'},
    2: {'date_to': '28.04', 'duration': 7, 'link': 'https://plus.tez-tour.com', 'price': '20 000'},
    3: {'date_to': '28.04', 'duration': 7, 'link': 'https://plus.tez-tour.com', 'price': '20 000'}
}

context = {
    'top_header': top_header, 'image_url': image_url, 'bottom_header': bottom_header,
    'description': description, 'from_to': from_to, 'tours': tours
}

def create_template(context):
    with open('jinja_template.html', 'w', encoding='utf-8') as res:
        res.write(template.render(context))
