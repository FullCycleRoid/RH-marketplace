from redis.asyncio import Redis

from src.core.config.config import settings

REDIS_URL = (
    f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}"
)


def get_redis_client() -> Redis:
    import redis.asyncio as aioredis

    pool = aioredis.ConnectionPool.from_url(
        REDIS_URL, max_connections=settings.MAX_POOL_CONNECTIONS, decode_responses=True
    )
    return aioredis.Redis(connection_pool=pool)


RedisPoolFactory = get_redis_client
