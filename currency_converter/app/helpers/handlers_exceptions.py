import aioredis
from ..exceptions import CurrencyNotFound, ParamNotFound, IncorrectRequestValue, RequestError
from .helpers import is_float
from typing import Dict, Tuple


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


def get_query(query) -> Tuple[str, str, float]:
    try:
        key_in_query('from', query)
        key_in_query('to', query)
        key_in_query('amount', query)
        value_is_letter(query['from'])
        value_is_letter(query['to'])
        value_is_float(query['amount'])
    except RequestError:
        raise
    else:
        return query['from'], query['to'], float(query['amount'])
