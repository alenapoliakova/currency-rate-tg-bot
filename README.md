# CurrencyRateTgBot
Телеграм бот для отправки пользователю курса валют с сайта ЦБ.

[![wakatime](https://wakatime.com/badge/github/alenapoliakova/CurrencyRateTgBot.svg)](https://wakatime.com/badge/github/alenapoliakova/CurrencyRateTgBot)
(с 6 марта)

## Инструкция по использованию:
1. Проверьте, что у вас установлен Python 3.10+.
2. Форкните репозиторий, а затем склонируйте.<br>
3. Для работы с ботом необходимо установить пакеты с помощью:<br>
<code>pip install -r requirements.txt</code><br>
Либо установите пакеты: pyTelegramBotAPI, requests, bs4, lxml с помощью команды:<br>
<code>pip install _package_name_</code>
4. Создайте файл settings.py, в котором будет информация о вашем боте. Пример файла settings.py:<br>
<code>BOT_TOKEN = 'token'</code><br>
<code>BOT_NAME = '@bot_name'</code><br>
\* инструкция по созданию тг бота и получению токена по ссылке: https://clck.ru/dWnJq
5. Запустите файл bot.py.

## Список команд:
- **/start** - начать общение с ботом
![img.png](images/img1.png)
- **/currency** - открывается inline-клавиатура с выбором предпочитаемой валюты
![img.png](images/img2.png)
- сообщение от бота после нажатия inline-кнопки:
![img.png](images/img3.png)