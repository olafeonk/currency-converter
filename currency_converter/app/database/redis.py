import aioredis
from typing import Dict

from ..helpers.handlers_exceptions import get_currency_rate


async def upload(data: Dict[str,  str], merge: bool) -> None:
    redis: aioredis.commands.Redis = await aioredis.create_redis_pool('redis://localhost')
    if not merge:
        await redis.flushdb(async_op=True)
    currency: str
    amount: str
    for currency, amount in data.items():
        await redis.set(currency.upper(), amount)
    redis.close()
    await redis.wait_closed()


async def convert(from_: str, to: str, amount: float) -> float:
    redis: aioredis.commands.Redis = await aioredis.create_redis_pool('redis://localhost')

    value_from = await get_currency_rate(from_, redis)
    value_to = await get_currency_rate(to, redis)
    redis.close()
    await redis.wait_closed()
    return amount * value_to / value_from

