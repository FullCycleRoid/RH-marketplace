from abc import ABC

from src.core.cache.interfaces.repositories import AbstractCacheRepository
from src.core.interfaces import AbstractUnitOfWork


class CacheUnitOfWork(AbstractUnitOfWork, ABC):
    cache: AbstractCacheRepository
