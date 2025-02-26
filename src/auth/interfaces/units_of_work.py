from abc import ABC

from src.auth.interfaces.repositories import (
    RefreshTokensRepository,
    UsersRepository,
    UserRolesRepository
)
from src.core.interfaces.units_of_work import AbstractUnitOfWork


class UsersUnitOfWork(AbstractUnitOfWork, ABC):
    users: UsersRepository
    refresh_tokens: RefreshTokensRepository
    user_roles: UserRolesRepository
