from typing import AsyncGenerator


from redis.asyncio.client import Redis

import config


async def get_redis() -> AsyncGenerator | None:
    redis_client = None

    try:
        redis_client: Redis | None = Redis(**config.REDIS_CONFIG)
        yield redis_client

    finally:
        if redis_client:
            await redis_client.aclose()
