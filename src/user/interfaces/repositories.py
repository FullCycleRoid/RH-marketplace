from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.core.database.declarative_base import Base
from src.core.interfaces.repositories import AbstractRepository
from src.user.models import RefreshToken, User, UserRole


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


class RefreshTokensRepository(AbstractRepository, ABC):

    @abstractmethod
    async def get_by_value(self, value: str) -> Optional[RefreshToken]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_valid_refresh_token(
        self, user_id: int
    ) -> Optional[RefreshToken]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID) -> Optional[RefreshToken]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: Base) -> RefreshToken:
        raise NotImplementedError

    @abstractmethod
    async def get(self, uuid: UUID) -> Optional[RefreshToken]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, uuid: UUID, model: Base) -> RefreshToken:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[RefreshToken]:
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
