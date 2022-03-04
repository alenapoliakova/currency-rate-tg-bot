# CurrencyRateTgBot
Телеграм бот, который отправляет пользователю официальный курс доллара/евро с сайта ЦБ.

# Инструкция по использованию бота:
1. Проверьте, что у вас установлен Python 3.10+.
2. Склонируйте репозиторий с помощью команды:<br>
<code>git clone https://github.com/alenapoliakova/CurrencyRateTgBot.git </code>
3. Для работы с ботом необходимо установить пакеты с помощью:<br>
<code>pip install -r requirements.txt</code><br>
Либо установите пакеты: pyTelegramBotAPI, requests, bs4, lxml с помощью команды:<br>
<code>pip install _package_name_</code>
4. Создайте файл settings.py, в котором будет информация о вашем боте. Пример файла settings.py:<br>
<code>BOT_TOKEN = 'token'</code><br>
<code>BOT_NAME = '@bot_name'</code><br>
\* инструкция по созданию тг бота и получению токена по ссылке: https://clck.ru/dWnJq
5. Запустите файл bot.py