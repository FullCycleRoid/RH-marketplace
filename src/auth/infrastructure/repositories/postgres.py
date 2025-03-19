from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import Result, delete, insert, select, update

from src.auth.infrastructure.repositories.interfaces import \
    RefreshTokensRepository
from src.core.database.declarative_base import Base
from src.core.database.repositories import SQLAlchemyRepository
from src.user.infrastructure.models import RefreshToken


class SQLAlchemyRefreshTokensRepository(SQLAlchemyRepository, RefreshTokensRepository):

    async def get_by_value(self, value: str) -> Optional[RefreshToken]:
        result: Result = await self._session.execute(
            select(RefreshToken).filter_by(refresh_token=value)
        )
        return result.scalar_one_or_none()

    async def get_user_valid_refresh_token(
        self, user_id: int
    ) -> Optional[RefreshToken]:
        result: Result = await self._session.execute(
            select(RefreshToken).filter(
                RefreshToken.user_id == user_id,
                RefreshToken.expires_at > datetime.now(),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_uuid(self, uuid: UUID) -> Optional[RefreshToken]:
        result: Result = await self._session.execute(
            select(RefreshToken).filter_by(uuid=uuid)
        )
        return result.scalar_one_or_none()

    async def get(self, uuid: UUID) -> Optional[RefreshToken]:
        result: Result = await self._session.execute(
            select(RefreshToken).filter_by(uuid=uuid)
        )
        return result.scalar_one_or_none()

    async def add(self, model: Base) -> RefreshToken:
        result: Result = await self._session.execute(
            insert(RefreshToken)
            .values(
                created_time=datetime.utcnow(),
                updated_time=datetime.utcnow(),
                **model.to_dict(exclude={"created_time", "updated_time"})
            )
            .returning(RefreshToken)
        )

        return result.scalar_one()

    async def update(self, uuid: UUID, model: Base) -> RefreshToken:
        result: Result = await self._session.execute(
            update(RefreshToken)
            .filter_by(uuid=uuid)
            .values(**model.to_dict(exclude={"uuid", "created_time", "updated_time"}))
            .returning(RefreshToken)
        )

        return result.scalar_one()

    async def delete(self, uuid: UUID) -> None:
        await self._session.execute(delete(RefreshToken).filter_by(uuid=uuid))

    async def list(self) -> List[RefreshToken]:
        result: Result = await self._session.execute(select(RefreshToken))
        return list(result.scalars().all())
