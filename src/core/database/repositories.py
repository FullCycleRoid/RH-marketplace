from abc import ABC

from src.core.database.session import AsyncSessionDep
from src.core.interfaces.repositories import AbstractRepository


class SQLAlchemyRepository(AbstractRepository, ABC):
    """
    Repository interface for SQLAlchemy, from which should be inherited all other repositories,
    which would be based on SQLAlchemy logics.
    """

    def __init__(self, session: AsyncSessionDep) -> None:
        self.session = session
