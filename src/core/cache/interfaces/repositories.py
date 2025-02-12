from abc import ABC, abstractmethod
from typing import Optional, Any

from src.core.cache.models import CacheModel


class AbstractCacheRepository(ABC):
    """
    Interface for any repository, which would be used for work with domain model, according DDD.

    Main purpose is to encapsulate internal logic that is associated with the use of one or another data
    storage scheme, for example, ORM.
    """

    @abstractmethod
    async def set_data(self, cache_data: CacheModel, is_transaction: bool = False) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, prefix: str, key: str) -> Optional[Any]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, prefix: str, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_all_prefix_keys(self, prefix: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_expiration(self, prefix: str, key: str, time: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def _build_key(self, prefix: str, key: str):
        return prefix + str(key)
