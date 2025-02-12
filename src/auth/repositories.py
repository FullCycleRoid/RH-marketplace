from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy import Result, delete, insert, select, update

from src.core.database.declarative_base import Base
from src.core.database.repositories import SQLAlchemyRepository
from src.auth.interfaces.repositories import RefreshTokensRepository, UsersRepository, UserRolesRepository
from src.auth.models import User, RefreshToken, UserRole


class SQLAlchemyUsersRepository(SQLAlchemyRepository, UsersRepository):
    async def get(self, id: int) -> Optional[User]:
        result: Result = await self._session.execute(select(User).filter_by(id=id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result: Result = await self._session.execute(select(User).filter_by(email=email))
        return result.scalar_one_or_none()

    async def get_by_telegram_username(self, telegram_username: str) -> Optional[User]:
        result: Result = await self._session.execute(select(User).filter_by(telegram_username=telegram_username))
        return result.scalar_one_or_none()

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        result: Result = await self._session.execute(select(User).filter_by(telegram_id=telegram_id))
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> Optional[User]:
        result: Result = await self._session.execute(select(User).filter_by(phone=phone))
        return result.scalar_one_or_none()

    async def add(self, model: Base) -> User:
        result: Result = await self._session.execute(
            insert(
                User
            ).values(
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                **model.to_dict(exclude={'id', 'created_at', 'updated_at'})
            ).returning(User)
        )

        return result.scalar_one()

    async def update(self, id: int, model: Base) -> User:
        result: Result = await self._session.execute(
            update(
                User
            ).filter_by(
                id=id
            ).values(
                **model.to_dict(
                    exclude={
                        'id',
                        'created_at',
                        'updated_at'
                    }
                )
            ).returning(
                User
            )
        )
        return result.scalar_one()

    async def delete(self, id: int) -> None:
        await self._session.execute(delete(User).filter_by(id=id))

    async def list(self) -> List[User]:
        result: Result = await self._session.execute(select(User))
        return list(result.scalars())


class SQLAlchemyRefreshTokensRepository(SQLAlchemyRepository, RefreshTokensRepository):

    async def get_by_value(self, value: str) -> Optional[RefreshToken]:
        result: Result = await self._session.execute(select(RefreshToken).filter_by(refresh_token=value))
        return result.scalar_one_or_none()

    async def get_user_valid_refresh_token(self, user_id: int) -> Optional[RefreshToken]:
        result: Result = await self._session.execute(
            select(
                RefreshToken
            ).filter(
                RefreshToken.user_id == user_id,
                RefreshToken.expires_at > datetime.now()
            )
        )
        return result.scalar_one_or_none()

    async def get_by_uuid(self, uuid: UUID) -> Optional[RefreshToken]:
        result: Result = await self._session.execute(select(RefreshToken).filter_by(uuid=uuid))
        return result.scalar_one_or_none()

    async def get(self, uuid: UUID) -> Optional[RefreshToken]:
        result: Result = await self._session.execute(select(RefreshToken).filter_by(uuid=uuid))
        return result.scalar_one_or_none()

    async def add(self, model: Base) -> RefreshToken:
        result: Result = await self._session.execute(
            insert(
                RefreshToken
            ).values(
                created_time=datetime.utcnow(),
                updated_time=datetime.utcnow(),
                **model.to_dict(exclude={'created_time', 'updated_time'})
            ).returning(
                RefreshToken
            )
        )

        return result.scalar_one()

    async def update(self, uuid: UUID, model: Base) -> RefreshToken:
        result: Result = await self._session.execute(
            update(RefreshToken).filter_by(uuid=uuid).values(**model.to_dict(exclude={'uuid', 'created_time', 'updated_time'})).returning(RefreshToken)
        )

        return result.scalar_one()

    async def delete(self, uuid: UUID) -> None:
        await self._session.execute(delete(RefreshToken).filter_by(uuid=uuid))

    async def list(self) -> List[RefreshToken]:
        result: Result = await self._session.execute(select(RefreshToken))
        return list(result.scalars().all())


class SQLAlchemyUserRolesRepository(SQLAlchemyRepository, UserRolesRepository):

    async def get(self, id: int) -> Optional[UserRole]:
        result: Result = await self._session.execute(select(UserRole).filter_by(id=id))
        return result.scalar_one_or_none()

    async def add(self, model: Base) -> UserRole:
        raise NotImplementedError

    async def update(self, id: int, model: Base) -> UserRole:
        raise NotImplementedError

    async def delete(self, id: int) -> None:
        raise NotImplementedError

    async def list(self) -> List[UserRole]:
        result: Result = await self._session.execute(select(UserRole))
        return list(result.scalars())
