import json
import logging

from redis.asyncio.client import Redis
from redis.commands.json.path import Path
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.exceptions import ResponseError

from src.model import redis_schema

logger = logging.getLogger(__name__)


class UserRedisDAL:
    """Data Access Layer для операций с пользователями в Redis"""

    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def clean_redis(self, tg_id: str):
        await self.redis_client.json().delete(f"user:{tg_id}")  # type: ignore

    async def create_index(self):
        index_name = "idx:user"
        index = self.redis_client.ft(index_name)
        try:
            await index.create_index(
                redis_schema,
                definition=IndexDefinition(prefix=["user:"], index_type=IndexType.JSON),
            )
            logging.info(f"Index {index_name} has been created")
        except ResponseError as exc:
            if exc.args[0] == "Index already exists":
                logging.info(exc.args[0])

    async def add_fields_to_user_data(self, *, tg_id: str, user_data: dict):
        if "tg_id" in user_data.keys():
            await self.redis_client.json().set(  # type: ignore
                f"user:{user_data['tg_id']}", Path.root_path(), user_data
            )
        else:
            await self.redis_client.json().mset(
                [
                    (  # type: ignore
                        f"user:{tg_id}",
                        f"$.{user_field}",
                        user_data[user_field],
                    )
                    for user_field in user_data.keys()
                ]
            )

        return await self.get_user(tg_id)

    async def get_user(self, tg_id: str) -> dict:
        user_from_redis = (
            await self.redis_client.ft(index_name="idx:user").search(tg_id)
        ).docs[0]  # type: ignore
        user_from_redis_dict = json.loads(user_from_redis.json)
        return user_from_redis_dict
