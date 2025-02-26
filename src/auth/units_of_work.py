from typing_extensions import Self

from src.core.database.units_of_work import SQLAlchemyUnitOfWork
from src.auth.interfaces.repositories import (
    RefreshTokensRepository,
    UsersRepository,
    UserRolesRepository
)
from src.auth.interfaces.units_of_work import UsersUnitOfWork
from src.auth.repositories import (
    SQLAlchemyRefreshTokensRepository,
    SQLAlchemyUsersRepository,
    SQLAlchemyUserRolesRepository
)


class SQLAlchemyUsersUnitOfWork(SQLAlchemyUnitOfWork, UsersUnitOfWork):

    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.users: UsersRepository = SQLAlchemyUsersRepository(session=self._session)
        self.refresh_tokens: RefreshTokensRepository = SQLAlchemyRefreshTokensRepository(session=self._session)
        self.manager_roles: UserRolesRepository = SQLAlchemyUserRolesRepository(session=self._session)
        return uow
