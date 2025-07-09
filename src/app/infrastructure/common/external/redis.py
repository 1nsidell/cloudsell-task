import redis.asyncio as redis

from app.infrastructure.common.config.config import RedisConfig


class RedisConnectionManager:
    def __init__(self, config: RedisConfig):
        self._url: str = config.url
        self._pool: redis.ConnectionPool
        self._redis: redis.Redis

    def startup(self) -> None:
        self._pool = redis.ConnectionPool.from_url(
            self._url,
            decode_responses=True,
        )
        self._redis = redis.Redis(connection_pool=self._pool)

    def get_connection(self) -> redis.Redis:
        return self._redis

    async def shutdown(self) -> None:
        if self._redis:
            await self._redis.aclose()
        if self._pool:
            await self._pool.disconnect()
