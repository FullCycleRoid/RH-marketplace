from typing import Callable

from redis.asyncio import Redis
from typing_extensions import Self

from src.core.cache.interfaces.repositories import AbstractCacheRepository
from src.core.cache.redis.repositories import RedisRepository
from src.core.cache.redis.utils import RedisPoolFactory
from src.core.interfaces.units_of_work import AbstractUnitOfWork


class RedisUnitOfWork(AbstractUnitOfWork):
    """
    Unit of work interface for Redis, from which should be inherited all other units of work,
    which would be based on Cache logics.
    """
    def __init__(self, pool_factory: Callable = RedisPoolFactory) -> None:
        self._pool_factory: Callable = pool_factory

    async def __aenter__(self) -> Self:
        self._connection_pool: Redis = self._pool_factory()
        self.cache: AbstractCacheRepository = RedisRepository(connection_pool=self._pool_factory())
        return await super().__aenter__()

    async def __aexit__(self, *args, **kwargs) -> None:
        await self._connection_pool.close()

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
