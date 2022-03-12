from telebot import TeleBot, types
from requests import get
from re import findall, match
from bs4 import BeautifulSoup as bs
from time import strftime, localtime
from settings import BOT_TOKEN, BOT_NAME
from collections import namedtuple


bot = TeleBot(BOT_TOKEN, parse_mode='html')
name = BOT_NAME

date = namedtuple('Date', ['day', 'month', 'year'])

db = {}
data = {
    'start': f'Привет! Бот <b>{name}</b> делится с вами курсом валют с <b>сайта ЦБ</b>.\n\n'
             f'Отправьте <b>/currency</b>, чтобы выбрать валюту.',
    'open_markup': 'Клавиатура открыта, выберите валюту.',
    'currency': 'Отправьте мне интересующую вас дату в формате: 02.02.2022, 02 02 2022, 02.02.22 или 02 02 22',
    'answer_to_user': 'Я не понял вас. Убедитесь, что ваша дата в формате день.месяц.год или день месяц год.',
    'close_markup': 'Вы закрыли клавиатуру. Отправьте <b>/currency</b>, чтобы открыть клавиатуру.',
    'not_in_dict': 'Вы ввели команду, которой нет в моём словаре. Отправьте <b>/start</b>, чтобы начать общение с ботом.'
}


def parse_date(actual_date: str) -> tuple | int:
    try:
        real_date = match(r'^[0-9]{1,2}[ .][0-9]{1,2}[ .][0-9]{4}', actual_date).group()
    except TypeError:
        return 0
    except AttributeError:  # Обработка ошибки для .group()
        return 0
    else:
        now_day, now_month, now_year = strftime("%d %m %Y", localtime()).split()

        if '.' in real_date:
            real_date = real_date.split('.')
        else:
            real_date = real_date.split()

        new_date = date(real_date[0], real_date[1], real_date[2])

        if int(new_date.year) > int(now_year):
            return 0
        elif int(new_date.year) == int(now_year) and int(new_date.month) > int(now_month):
            return 0
        elif int(new_date.year) == int(now_year) and int(new_date.month) == int(now_month) and int(new_date.day) > int(now_day):
            return 0

        return new_date


def get_currency(actual_currency: str, date_to_parse: tuple):
    """
    Функция для парсинга курса ЦБ. Если данный курс уже парсился, то данные возьмутся из словаря db.
    :param actual_currency: Имя валюты.
    :param date_to_parse: Кортеж, который содержит дату для парсинга.
    :return: Текст с именем валюты и её курсом.
    """
    day, month, year = date_to_parse.day, date_to_parse.month, date_to_parse.year
    # day, month, year = strftime("%d %m %Y", localtime()).split()

    currency = db.get(f'{day} {month} {year} {actual_currency}', None)
    if currency:
        return f'Курс <b>{currency[0]}</b> на {day}.{month}.{year}: {currency[1]}'
    else:
        url = f'https://cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}'

        request = get(url)
        soup = bs(request.text, 'lxml')

        for tag in soup.findAll('valute'):
            result = tag.get_text(strip=True)
            name_of_currency = ' '.join(findall(r'[а-яА-я]+', result))

            numbers = findall(r'[0-9]+', result)
            price = f'{numbers[-2]}.{numbers[-1]}'

            if actual_currency in name_of_currency:
                db[f'{day} {month} {year} {actual_currency}'] = (name_of_currency, price)
                return f'Курс <b>{name_of_currency}</b> на {day}.{month}.{year}: {price}₽'


@bot.message_handler(commands='start')
def start(message):
    bot.send_message(message.chat.id, data['start'])


@bot.message_handler(commands='currency')
def currency(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    button_1 = types.KeyboardButton('Курс Доллара США 💲')
    button_2 = types.KeyboardButton('Курс Евро 💶')
    button_3 = types.KeyboardButton('Курс Фунта стерлингов 💷')
    button_4 = types.KeyboardButton('Курс Белорусского рубля 🇧🇾')
    button_5 = types.KeyboardButton('Назад')

    markup.add(button_1, button_2, button_3, button_4, button_5)

    bot.send_message(message.chat.id, data['open_markup'], reply_markup=markup)


def answer_to_user(message, **kwargs):
    # TODO: распарсить здесь дату и добавить в get_currency выбор даты

    parsed_date = parse_date(actual_date=message.text)

    if isinstance(parsed_date, date):
        bot.send_message(message.chat.id, get_currency(actual_currency=kwargs['valute'], date_to_parse=parsed_date))
    else:
        bot.send_message(message.chat.id, data['answer_to_user'])


@bot.message_handler(content_types='text')
def reply(message):

    match message.text:
        case 'Курс Доллара США 💲':
            msg = bot.send_message(message.chat.id, data['currency'])
            bot.register_next_step_handler(message=msg, callback=answer_to_user, valute='Доллар США')
        case 'Курс Евро 💶':
            msg = bot.send_message(message.chat.id, data['currency'])
            bot.register_next_step_handler(message=msg, callback=answer_to_user, valute='Евро')
        case 'Курс Фунта стерлингов 💷':
            msg = bot.send_message(message.chat.id, data['currency'])
            bot.register_next_step_handler(message=msg, callback=answer_to_user, valute='Фунт стерлингов')
        case 'Курс Белорусского рубля 🇧🇾':
            msg = bot.send_message(message.chat.id, data['currency'])
            bot.register_next_step_handler(message=msg, callback=answer_to_user, valute='Белорусский рубль')
        case 'Назад':  # Закрытие клавиатуры
            bot.send_message(message.chat.id, data['close_markup'], reply_markup=types.ReplyKeyboardRemove())
        case _:
            bot.send_message(message.chat.id, data['not_in_dict'])


bot.polling(non_stop=True)
