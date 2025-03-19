from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.database.declarative_base import Base
from src.core.interfaces.repositories import AbstractRepository
from src.user.infrastructure.models import User, UserRole


class UsersRepository(AbstractRepository, ABC):

    @abstractmethod
    async def get_by_phone(self, phone: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_telegram_username(self, telegram_username: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: Base) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, model: Base) -> User:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[User]:
        raise NotImplementedError


class UserRolesRepository(AbstractRepository, ABC):

    @abstractmethod
    async def add(self, model: Base) -> UserRole:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Optional[UserRole]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, model: Base) -> UserRole:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[UserRole]:
        raise NotImplementedError
