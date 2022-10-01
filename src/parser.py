import requests
from bs4 import BeautifulSoup as bs
from re import findall
from time import strftime, localtime

from data import rate_cache


def get_currency(actual_currency: str) -> str:
    """
    Парсинг курса ЦБ. Если данный курс уже парсился, то данные возьмутся из кэша.
    :param actual_currency: Название валюты.
    :return: Текст с именем валюты и её курсом.
    """
    day, month, year = strftime("%d %m %Y", localtime()).split()
    currency = rate_cache.get(f"{day} {month} {year} {actual_currency}")

    if currency:
        return f"Курс *{currency[0]}* на {day}.{month}.{year}: {currency[1]}"

    url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}"

    request = requests.get(url)
    soup = bs(request.text, "lxml")

    for tag in soup.findAll("valute"):
        result = tag.get_text(strip=True)
        name_of_currency = " ".join(findall(r"[а-яА-я]+", result))

        numbers = findall(r"\d+", result)
        price = f"{numbers[-2]}.{numbers[-1]}"

        if actual_currency in name_of_currency:
            rate_cache[f"{day} {month} {year} {actual_currency}"] = (name_of_currency, price)
            return f"Курс *{name_of_currency}* на {day}.{month}.{year}: {price}"
