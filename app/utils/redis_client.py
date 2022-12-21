from typing import Protocol

import redis.asyncio as redis
from datetime import datetime

from async_cb_rate.models import Currency


class BaseRateHandler(Protocol):

    async def add_currency(self, currency: Currency) -> None: ...

    async def get_currency(self, code: str, date: datetime) -> Currency | None: ...

    @staticmethod
    def convert_to_date(date: datetime) -> str:
        return f"{date.year}:{date.month}:{date.day}"


class InMemoryRateHandler(BaseRateHandler):

    def __init__(self):
        self.cache: dict[str, str] = {}

    async def add_currency(self, currency: Currency) -> None:
        key = f"{currency.code}:{self.convert_to_date(currency.date)}"
        self.cache[key] = f"{currency.name}:{currency.price}"

    async def get_currency(self, code: str, date: datetime) -> Currency | None:
        if (rate_value := self.cache.get(f"{code}:{self.convert_to_date(date)}")) is None:
            return
        name, price = rate_value.split(":")
        return Currency(name=name, code=code, price=price, date=date)


class RedisRateHandler(BaseRateHandler):

    def __init__(self, host: str, port: int, db_num=0):
        self.redis = redis.Redis(host=host, port=port, db=db_num, decode_responses=True)

    async def add_currency(self, currency: Currency) -> None:
        key = f"{currency.code}:{self.convert_to_date(currency.date)}"
        await self.redis.set(key, f"{currency.name}:{currency.price}")

    async def get_currency(self, code: str, date: datetime) -> Currency | None:
        if (rate_value := await self.redis.get(f"{code}:{self.convert_to_date(date)}")) is None:
            return
        name, price = rate_value.split(":")
        return Currency(name=name, code=code, price=price, date=date)
