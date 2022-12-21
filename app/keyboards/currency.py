from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

key_map = {
    "Доллар США": "USD",
    "Евро": "EUR",
    "Фунт стерлингов": "GBP",
    "Белорусский рубль": "BYN",
}

kb = [
    [KeyboardButton(text="Доллар США"), KeyboardButton(text="Евро")],
    [KeyboardButton(text="Фунт стерлингов"), KeyboardButton(text="Белорусский рубль")],
    [KeyboardButton(text="Назад")],
]

keyboard = ReplyKeyboardMarkup(keyboard=kb)
button_names = key_map.keys()
