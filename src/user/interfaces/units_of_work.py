from abc import ABC

from src.core.interfaces.units_of_work import AbstractUnitOfWork
from src.user.interfaces.repositories import (
    RefreshTokensRepository,
    UserRolesRepository,
    UsersRepository,
)


class UsersUnitOfWork(AbstractUnitOfWork, ABC):
    users: UsersRepository
    refresh_tokens: RefreshTokensRepository
    user_roles: UserRolesRepository
