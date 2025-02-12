from typing import List

from sqlalchemy.sql import text
from sqlalchemy import Result

from src.auth.models import User
from src.core.database.units_of_work import SQLAlchemyUnitOfWork
from src.auth.sql_statements import (
    get_user_by_id_stmt,
    get_all_users_stmt
)


class AuthViews:
    def __init__(self, uow: SQLAlchemyUnitOfWork) -> None:
        self._uow: SQLAlchemyUnitOfWork = uow

    async def get_user_by_id(self, user_id: int) -> User:
        async with self._uow as uow:
            cursor: Result = await uow._session.execute(
                text(
                    get_user_by_id_stmt
                ).params(
                    user_id=user_id
                )
            )
            return User(**cursor.mappings().first())

    async def get_all_users(self) -> List[User]:
        async with self._uow as uow:
            cursor: Result = await uow._session.execute(
                text(
                    get_all_users_stmt
                )
            )
            return [User(**user) for user in cursor.mappings().all()]
