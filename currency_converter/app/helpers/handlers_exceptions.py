import aioredis
from ..exceptions import CurrencyNotFound, ParamNotFound, IncorrectRequestValue
from .helpers import is_float
from typing import Dict


async def get_currency_rate(currency: str, redis: aioredis.commands.Redis) -> float:
    if not await redis.exists(currency):
        raise CurrencyNotFound(currency)
    return float((await redis.get(currency)).decode('utf-8'))


def key_in_query(param: str, query) -> None:
    if param not in query:
        raise ParamNotFound(param)


def value_is_letter(value: str) -> None:
    if not value.isalpha():
        raise IncorrectRequestValue(value, 'string consisting of letters')


def value_is_float(value: str) -> None:
    if not is_float(value):
        raise IncorrectRequestValue(value, 'float')


def correct_data(data: Dict[str, str]) -> None:
    for key, value in data.items():
        value_is_letter(key)
        value_is_float(value)
