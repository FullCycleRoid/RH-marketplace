from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.database.declarative_base import Base


class AbstractRepository(ABC):
    """
    Interface for any repository, which would be used for work with domain model, according DDD.

    Main purpose is to encapsulate internal logic that is associated with the use of one or another data
    storage scheme, for example, ORM.
    """

    @abstractmethod
    async def add(self, model: Base) -> Base:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Optional[Base]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, model: Base) -> Base:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[Base]:
        raise NotImplementedError
