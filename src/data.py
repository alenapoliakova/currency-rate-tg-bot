from settings import config

LOGGER_FORMAT = "%(asctime)s %(levelname)s %(message)s"
LOGGER_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

rate_cache = {}
commands = {
    "start": f"Привет! Бот <b>{config.BOT_NAME}</b> делится с вами курсом валют с сайта ЦБ.\n\n"
             f"Отправьте <b>/currency</b>, чтобы выбрать валюту.",
    "open_markup": "Выберите валюту:",
    "currency": "Отправьте мне интересующую вас дату в формате: 02.02.2022, 02 02 2022, 02.02.22 или 02 02 22.",
    "answer_to_user": "Я не понял вас. Убедитесь, что дата в формате день.месяц.год или день месяц год.",
    "close_markup": "Вы закрыли клавиатуру. Отправьте */currency*, чтобы открыть клавиатуру.",
    "unknown_command": "Вы отправили неизвестную мне команду. Отправьте */start* для начала общения с ботом.",
}
