from telebot import TeleBot, types

from parser import get_currency, parse_date, date
from data import commands
from logger import Logger
from settings import config

bot = TeleBot(config.BOT_TOKEN, parse_mode="markdown")
log = Logger(config.LOG_FILE_PATH)
log.info("Bot started")


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, commands["start"], parse_mode="html")
    log.info(f"START user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>")


@bot.message_handler(commands=["currency"])
def currency(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    button_1 = types.KeyboardButton("Курс Доллара США 💲")
    button_2 = types.KeyboardButton("Курс Евро 💶")
    button_3 = types.KeyboardButton("Курс Фунта стерлингов 💷")
    button_4 = types.KeyboardButton("Курс Белорусского рубля 🇧🇾")
    button_5 = types.KeyboardButton("Назад")

    markup.add(button_1, button_2, button_3, button_4, button_5)
    bot.send_message(message.chat.id, commands["open_markup"], reply_markup=markup)
    log.info(f"CURRENCY user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>")


def answer_to_user(message, **kwargs):
    parsed_date = parse_date(actual_date=message.text)

    if isinstance(parsed_date, date):
        bot.send_message(message.chat.id, get_currency(actual_currency=kwargs["valute"], date_to_parse=parsed_date))
    else:
        bot.send_message(message.chat.id, commands["answer_to_user"])


@bot.message_handler(content_types=["text"])
def reply(message):
    match message.text:
        case "Курс Доллара США 💲":
            msg = bot.send_message(message.chat.id, commands["currency"])
            bot.register_next_step_handler(message=msg, callback=answer_to_user, valute="Доллар США")
        case "Курс Евро 💶":
            msg = bot.send_message(message.chat.id, commands["currency"])
            bot.register_next_step_handler(message=msg, callback=answer_to_user, valute="Евро")
        case "Курс Фунта стерлингов 💷":
            msg = bot.send_message(message.chat.id, commands["currency"])
            bot.register_next_step_handler(message=msg, callback=answer_to_user, valute="Фунт стерлингов")
        case "Курс Белорусского рубля 🇧🇾":
            msg = bot.send_message(message.chat.id, commands["currency"])
            bot.register_next_step_handler(message=msg, callback=answer_to_user, valute="Белорусский рубль")
        case "Назад":
            # Закрытие клавиатуры
            bot.send_message(message.chat.id, commands["close_markup"], reply_markup=types.ReplyKeyboardRemove())
        case _:
            bot.send_message(message.chat.id, commands["unknown_command"])
    log.info(f"TEXT user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>, "
             f"text={message.text}")


bot.polling(non_stop=True)
log.info("Bot finished")
