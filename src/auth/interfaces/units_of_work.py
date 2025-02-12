from abc import ABC

from src.core.interfaces import AbstractUnitOfWork
from src.auth.interfaces.repositories import (
    RefreshTokensRepository,
    UsersRepository,
    UserRolesRepository
)


class UsersUnitOfWork(AbstractUnitOfWork, ABC):
    users: UsersRepository
    refresh_tokens: RefreshTokensRepository
    user_roles: UserRolesRepository
