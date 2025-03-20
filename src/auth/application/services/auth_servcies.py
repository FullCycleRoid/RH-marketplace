from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from src.auth.exceptions import RefreshTokenNotFound, RefreshTokenNotValid
from src.auth.infrastructure.models import RefreshToken, User
from src.auth.infrastructure.repositories.postgres import \
    SQLAlchemyRefreshTokensRepository


class AuthService:
    def __init__(self, refresh_repository: SQLAlchemyRefreshTokensRepository) -> None:
        self.refresh_repository = refresh_repository

    async def create_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        refresh_token: RefreshToken = await self.refresh_repository.refresh_tokens.add(
            refresh_token
        )
        await self.refresh_repository.commit()
        return refresh_token

    async def get_refresh_token_by_uuid(self, uuid: UUID) -> RefreshToken:
        refresh_token: Optional[RefreshToken] = (
            await self.refresh_repository.refresh_tokens.get_by_uuid(uuid=uuid)
        )
        if not refresh_token:
            raise RefreshTokenNotValid

        return refresh_token

    async def check_refresh_token_existence(
        self, uuid: Optional[UUID] = None, value: Optional[str] = None
    ) -> bool:
        if not (uuid or value):
            raise ValueError("Требуется передать значени или UUID токена")

        refresh_token: Optional[RefreshToken]
        if uuid:
            refresh_token = await self.refresh_repository.refresh_tokens.get_by_uuid(
                uuid=uuid
            )
            if refresh_token:
                return True

        if value:
            refresh_token = await self.refresh_repository.refresh_tokens.get_by_value(
                value=value
            )
            if refresh_token:
                return True

        return False

    async def get_refresh_token_by_value(self, value: str) -> RefreshToken:
        refresh_token: Optional[RefreshToken] = (
            await self.refresh_repository.refresh_tokens.get_by_value(value)
        )
        if not refresh_token:
            raise RefreshTokenNotValid

        return refresh_token

    async def expire_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        refresh_token.expires_at = datetime.utcnow() - timedelta(days=1)
        refresh_token: RefreshToken = (
            await self.refresh_repository.refresh_tokens.update(
                uuid=refresh_token.uuid, model=refresh_token
            )
        )
        await self.refresh_repository.commit()
        return refresh_token

    async def get_old_valid_refresh_token(self, user: User) -> RefreshToken:
        refresh_token: Optional[RefreshToken] = (
            await self.refresh_repository.refresh_tokens.get_user_valid_refresh_token(
                user_id=user.id
            )
        )
        if not refresh_token:
            raise RefreshTokenNotFound

        return refresh_token

    async def check_old_valid_refresh_token_existence(self, user: User) -> bool:
        refresh_token: Optional[RefreshToken] = (
            await self.refresh_repository.refresh_tokens.get_user_valid_refresh_token(
                user_id=user.id
            )
        )
        if refresh_token:
            return True

        return False
