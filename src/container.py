from dependency_injector import containers, providers

from src.dal import UserRedisDAL
from src.redis_init import get_redis


class RedisContainer(containers.DeclarativeContainer):
    redis_pool = providers.Resource(get_redis)

    redis_user_dal = providers.Factory(UserRedisDAL, redis_client=redis_pool)
