from typing import List

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from src import User


class UserViews:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User:
        get_user_by_id_stmt = ""
        cursor: Result = await self.session.execute(
            text(get_user_by_id_stmt).params(user_id=user_id)
        )
        return User(**cursor.mappings().first())

    async def get_all_users(self) -> List[User]:
        get_all_users_stmt = ""
        cursor: Result = await self.session.execute(text(get_all_users_stmt))
        return [User(**user) for user in cursor.mappings().all()]
