from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing_extensions import Self

from src.core.database.postgres.connectors import PsycopgAsyncSessionFactory
from src.core.interfaces.units_of_work import AbstractUnitOfWork


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    """
    Unit of work interface for SQLAlchemy, from which should be inherited all other units of work,
    which would be based on SQLAlchemy logics.
    """

    def __init__(
        self, session_factory: async_sessionmaker = PsycopgAsyncSessionFactory
    ) -> None:
        self._session_factory: async_sessionmaker = session_factory

    async def __aenter__(self) -> Self:
        self._session: AsyncSession = self._session_factory()
        return await super().__aenter__()

    async def __aexit__(self, *args, **kwargs) -> None:
        await super().__aexit__(*args, **kwargs)
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        """
        Rollbacks all uncommited changes.

        Uses self._session.expunge_all() to avoid sqlalchemy.orm.exc.DetachedInstanceError after session rollback,
        due to the fact that selected object is cached by Session. And self._session.rollback() deletes all Session
        cache, which causes error on Domain model, which is not bound now to the session and can not retrieve
        attributes.

        https://pythonhint.com/post/1123713161982291/how-does-a-sqlalchemy-object-get-detached
        """

        self._session.expunge_all()
        await self._session.rollback()


class MongoDBUnitOfWork(AbstractUnitOfWork):
    """
    Unit of work interface for MongoDB, from which should be inherited all other units of work,
    which would be based on MongoDB logics.
    """

    async def __aenter__(self) -> Self:
        return await super().__aenter__()

    async def __aexit__(self, *args, **kwargs) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
