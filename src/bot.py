from telebot import TeleBot, types

from parser import get_currency
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

    button_1 = types.KeyboardButton("Курс Доллара США")
    button_2 = types.KeyboardButton("Курс Евро")
    button_3 = types.KeyboardButton("Назад")

    markup.add(button_1, button_2, button_3)
    bot.send_message(message.chat.id, commands["open_markup"], reply_markup=markup)
    log.info(f"CURRENCY user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>")


@bot.message_handler(content_types=["text"])
def reply(message):
    match message.text:
        case "Курс Доллара США":
            bot.send_message(message.chat.id, get_currency("Доллар США"))
        case "Курс Евро":
            bot.send_message(message.chat.id, get_currency("Евро"))
        case "Назад":
            bot.send_message(message.chat.id, commands["close_markup"], reply_markup=types.ReplyKeyboardRemove())
        case _:
            bot.send_message(message.chat.id, commands["unknown_command"])
    log.info(f"TEXT user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>, "
             f"text={message.text}")


bot.polling(non_stop=True)
log.info("Bot finished")
