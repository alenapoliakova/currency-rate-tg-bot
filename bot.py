from telebot import TeleBot, types
from requests import get
from re import findall
from bs4 import BeautifulSoup as bs
from time import strftime, localtime
from settings import BOT_TOKEN, BOT_NAME


bot = TeleBot(BOT_TOKEN, parse_mode='html')
name = BOT_NAME


db = {}
data = {
    'start': f'Привет! Бот <b>{name}</b> делится с вами курсом валют с <b>сайта ЦБ</b>.\n\nОтправьте <b>/currency</b>, чтобы выбрать валюту.',
    'open_markup': 'Откройте клавиатуру для выбора валюты.',
    'close_markup': 'Вы закрыли клавиатуру. Отправьте <b>/currency</b>, чтобы открыть клавиатуру.'
}


def get_currency(actual_currency: str):
    """
    Функция для парсинга курса ЦБ. Если данные курс валюты уже парсился, то данные возьмутся из словаря db.
    :param actual_currency: Имя валюты.
    :return: Текст с именем валюты и её курсом.
    """
    day, month, year = strftime("%d %m %Y", localtime()).split()

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
                return f'Курс <b>{name_of_currency}</b> на {day}.{month}.{year}: {price}'


@bot.message_handler(commands='start')
def start(message):
    bot.send_message(message.chat.id, data['start'])


@bot.message_handler(commands='currency')
def currency(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    button_1 = types.KeyboardButton('Курс Доллара США')
    button_2 = types.KeyboardButton('Курс Евро')
    button_3 = types.KeyboardButton('Назад')

    markup.add(button_1, button_2, button_3)

    bot.send_message(message.chat.id, data['open_markup'], reply_markup=markup)


@bot.message_handler(content_types='text')
def reply(message):
    match message.text:
        case 'Курс Доллара США':
            bot.send_message(message.chat.id, get_currency('Доллар США'))
        case 'Курс Евро':
            bot.send_message(message.chat.id, get_currency('Евро'))
        case 'Назад':
            bot.send_message(message.chat.id, data['close_markup'],reply_markup=types.ReplyKeyboardRemove())


bot.polling(non_stop=True)
