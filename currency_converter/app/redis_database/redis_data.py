import aioredis
from typing import Dict

from .exceptions.exceptions import DataBaseError


async def upload(data: Dict[str,  str], merge: bool) -> None:
    redis: commands.Redis = await create_redis_pool('redis://localhost')
    if not merge:
        await redis.flushdb(async_op=True)
    currency: str
    amount: str
    for currency, amount in data.items():
        await redis.set(currency.upper(), amount)
    redis.close()
    await redis.wait_closed()


async def convert(from_: str, to: str, amount: float) -> float:
    redis: commands.Redis = await create_redis_pool('redis://localhost')
    if not await redis.exists(from_):
        raise DataBaseError(from_, 'not exists in database')
    if not await redis.exists(to):
        raise (to, 'not exists in database')
    value_from = float((await redis.get(from_)).decode('utf-8'))
    value_to = float((await redis.get(to)).decode('utf-8'))
    redis.close()
    await redis.wait_closed()
    return amount * value_to / value_from
