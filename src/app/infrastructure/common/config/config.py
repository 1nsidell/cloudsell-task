import os

from pydantic import BaseModel


class RedisConfig(BaseModel):
    """Config to connect to Redis database"""

    HOST: str = os.getenv("REDIS_HOST", "localhost")
    PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    DB: int = int(os.getenv("REDIS_DB", "0"))

    @property
    def url(self) -> str:
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"


class Configs:
    redis: RedisConfig = RedisConfig()


def get_configs() -> Configs:
    return Configs()
