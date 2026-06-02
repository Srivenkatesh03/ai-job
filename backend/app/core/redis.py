import logging
from typing import AsyncGenerator
import redis.asyncio as aioredis
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisManager:
    """Manages Redis connection pooling and client sessions for async application logic."""

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.pool = None

    def init_pool(self) -> None:
        """Initialize the async connection pool."""
        if not self.pool:
            logger.info(f"Initializing Redis connection pool at {self.redis_url}")
            self.pool = aioredis.ConnectionPool.from_url(
                self.redis_url,
                decode_responses=True,
                max_connections=50,
            )

    async def close(self) -> None:
        """Close the Redis pool."""
        if self.pool:
            logger.info("Closing Redis connection pool")
            await self.pool.disconnect()
            self.pool = None

    def get_client(self) -> aioredis.Redis:
        """Retrieve a Redis client instance from the pool."""
        if not self.pool:
            self.init_pool()
        return aioredis.Redis(connection_pool=self.pool)


redis_manager = RedisManager(settings.REDIS_URL)


async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    """Dependency to retrieve an async Redis client instance."""
    client = redis_manager.get_client()
    try:
        yield client
    finally:
        await client.close()
