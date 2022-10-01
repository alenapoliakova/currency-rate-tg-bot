from settings import config

LOGGER_FORMAT = "%(asctime)s %(levelname)s %(message)s"
LOGGER_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

rate_cache = {}
commands = {
    "start": f"Привет! Бот <b>{config.BOT_NAME}</b> делится с вами курсом валют с сайта ЦБ.\n\n"
             f"Отправьте <b>/currency</b>, чтобы выбрать валюту.",
    "open_markup": "Выберите валюту:",
    "close_markup": "Вы закрыли клавиатуру. Отправьте */currency*, чтобы открыть клавиатуру.",
    "unknown_command": "Вы отправили неизвестную мне команду. Отправьте */currency* для получения информации "
                       "о курсе валют.",
}
