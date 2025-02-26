import ast
from typing import Optional, Any

from redis.asyncio import Redis

from src.core.cache.interfaces.repositories import AbstractCacheRepository
from src.core.cache.models import CacheModel
from src.core.exceptions import RedisKeyNotFound


class RedisRepository(AbstractCacheRepository):
    """
    Repository interface for Redis, from which should be inherited all other repositories,
    which would be based on Redis logics.
    """
    def __init__(self, connection_pool) -> None:
        self.connection_pool: Redis = connection_pool

    async def set_data(self, cache_data: CacheModel, is_transaction: bool = False) -> None:
        async with self.connection_pool.pipeline(transaction=is_transaction) as pipe:
            await pipe.set(cache_data.key, cache_data.value)
            if cache_data.ttl:
                await pipe.expire(cache_data.key, cache_data.ttl)

            await pipe.execute()

    async def get(self, prefix: str, key: str) -> Optional[Any]:
        key: str = self._build_key(prefix, key)
        stored_obj: str = await self.connection_pool.get(key)
        try:
            return ast.literal_eval(stored_obj)
        except Exception:
            raise RedisKeyNotFound

    async def delete(self, prefix: str, key: str) -> None:
        key: str = self._build_key(prefix, key)
        return await self.connection_pool.delete(key)

    async def delete_all_prefix_keys(self, prefix: str) -> None:
        async for key in self.connection_pool.scan_iter(f"{prefix}*"):
            await self.connection_pool.delete(key)

    async def set_expiration(self, prefix: str, key: str, time: int) -> None:
        key: str = self._build_key(prefix, key)
        return await self.connection_pool.expire(key, time)

    def _build_key(self, prefix: str, key: str):
        return super()._build_key(prefix=prefix, key=key)
