import re

import requests
from collections import namedtuple
from bs4 import BeautifulSoup as bs
from time import strftime, localtime

from data import rate_cache

date = namedtuple("Date", ["day", "month", "year"])
compiled_date_pattern = re.compile(r"^[0-9]{1,2}[ .][0-9]{1,2}[ .][0-9]{4}")
compiled_letters_pattern = re.compile(r"[а-яА-я]+")
compiled_numbers_pattern = re.compile(r"\d+")


def parse_date(actual_date: str) -> date | None:
    try:
        real_date = compiled_date_pattern.match(actual_date).group()
    except TypeError:
        return
    except AttributeError:  # Обработка ошибки для .group()
        return
    else:
        day, month, year = strftime("%d %m %Y", localtime()).split()
        today = date(day, month, year)

        if "." in real_date:
            real_date = real_date.split(".")
        else:
            real_date = real_date.split()

        new_date = date(real_date[0], real_date[1], real_date[2])

        # 01.10.2023 (now is 01.10.2022), the year hasn't come yet
        if int(new_date.year) > int(today.year):
            return

        # 01.11.2022 (now is 01.10.2022), the month in year hasn't come yet
        if int(new_date.year) == int(today.year) and int(new_date.month) > int(today.month):
            return

        # 10.10.2022 (now is 01.10.2022), the day hasn't come yet in the actual month and year
        if int(new_date.year) == int(today.year) and int(new_date.month) == int(today.month):
            if int(new_date.day) > int(today.day):
                return

        return new_date


def get_currency(actual_currency: str, date_to_parse: date) -> str:
    """
    Парсинг курса ЦБ. Если данный курс уже парсился, то данные возьмутся из кэша.
    :param actual_currency: Название валюты.
    :param date_to_parse: Дата курса.
    :return: Текст с именем валюты и её курсом.
    """
    day, month, year = date_to_parse.day, date_to_parse.month, date_to_parse.year

    currency = rate_cache.get(f"{day} {month} {year} {actual_currency}")

    if currency:
        return f"Курс *{currency[0]}* на {day}.{month}.{year}: {currency[1]}"

    url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}"

    request = requests.get(url)
    soup = bs(request.text, "lxml")

    for tag in soup.findAll("valute"):
        result = tag.get_text(strip=True)
        currency_name = " ".join(compiled_letters_pattern.findall(result))
        numbers = compiled_numbers_pattern.findall(result)

        price = f"{numbers[-2]}.{numbers[-1]}"

        if actual_currency in currency_name:
            rate_cache[f"{day} {month} {year} {actual_currency}"] = (currency_name, price)
            return f"Курс *{currency_name}* на {day}.{month}.{year}: {price}"
