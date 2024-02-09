import asyncio

from dependency_injector.wiring import Provide, inject

from src.container import RedisContainer
from src.dal import UserRedisDAL


@inject
async def create_index(
    redis_client: UserRedisDAL = Provide[RedisContainer.redis_user_dal]
):
    return await redis_client.create_index()


async def main():
    redis_container = RedisContainer()
    redis_container.init_resources()
    redis_container.wire(modules=[__name__])
    return await create_index()


if __name__ == "__main__":
    asyncio.run(main())
