import pickle
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

from src.auth.infrastructure.models import RefreshToken
from src.config import settings
from src.core.cache.redis.DTO import CacheModel

from src.core.cache.redis.repositories import RedisRepository
from src.core.exceptions import RedisKeyNotFound
from src.user.exceptions import RefreshTokenNotFound, RefreshTokenNotValid, UserNotFound
from src.user.infrastructure.models import User, UserRole
from src.user.infrastructure.repositories.postgres import SQLAlchemyUsersRepository


class AuthService:
    def __init__(self, repo: SQLAlchemyUsersRepository) -> None:
        self.repo = repo

    async def check_user_existence(
        self,
        id: Optional[int] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        telegram_username: Optional[str] = None,
        telegram_id: Optional[int] = None,
    ) -> bool:

        if not (id or email or phone or telegram_username or telegram_id):
            raise ValueError(
                "Требуется передать адрес электронной почты, телефон, ID пользователя, "
                "telegram имя пользователя или telegram ID"
            )

        user: Optional[User]  # declaring here for mypy passing
        if id:
            user = await self.repo.users.get(id=id)
            if user:
                return True

        if email:
            user = await self.repo.users.get_by_email(email)
            if user:
                return True

        if phone:
            user = await self.repo.users.get_by_phone(phone)
            if user:
                return True

        if telegram_username:
            user = await self.repo.users.get_by_telegram_username(telegram_username)
            if user:
                return True

        if telegram_id:
            user = await self.repo.users.get_by_telegram_id(telegram_id)
            if user:
                return True

        return False

    async def register_user(self, user: User) -> User:
        user: User = await self.repo.users.add(user)
        await self.repo.commit()
        return user

    async def verify_user_email(self, user: User) -> User:
        user.is_email_confirmed = True
        user: User = await self.repo.users.update(id=user.id, model=user)
            await self.repo.commit()
            return user

    async def get_user_by_id(self, id: int) -> User:
        user: Optional[User] = await self.repo.users.get(id=id)
        if not user:
            raise UserNotFound
    
        return user

    async def get_user_by_email(self, email: str) -> User:
        user: Optional[User] = await self.repo.users.get_by_email(email=email)
        if not user:
            raise UserNotFound

        return user

    async def get_user_by_optional_email(self, email: str) -> Optional[User]:
        return await self.repo.users.get_by_email(email=email)

    async def get_user_by_phone(self, phone: str) -> User:
        user: Optional[User] = await self.repo.users.get_by_phone(phone=phone)
        if not user:
            raise UserNotFound

        return user

    async def create_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        refresh_token: RefreshToken = await self.repo.refresh_tokens.add(refresh_token)
        await self.repo.commit()
        return refresh_token

    async def get_refresh_token_by_uuid(self, uuid: UUID) -> RefreshToken:
        refresh_token: Optional[RefreshToken] = (
            await self.repo.refresh_tokens.get_by_uuid(uuid=uuid)
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
            refresh_token = await self.repo.refresh_tokens.get_by_uuid(uuid=uuid)
            if refresh_token:
                return True

        if value:
            refresh_token = await self.repo.refresh_tokens.get_by_value(value=value)
            if refresh_token:
                return True

        return False

    async def get_refresh_token_by_value(self, value: str) -> RefreshToken:
        refresh_token: Optional[RefreshToken] = (
            await self.repo.refresh_tokens.get_by_value(value)
        )
        if not refresh_token:
            raise RefreshTokenNotValid

        return refresh_token

    async def expire_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        refresh_token.expires_at = datetime.utcnow() - timedelta(days=1)
        refresh_token: RefreshToken = await self.repo.refresh_tokens.update(
            uuid=refresh_token.uuid, model=refresh_token
        )
        await self.repo.commit()
        return refresh_token

    async def update_user_profile(self, user: User) -> User:
        user: User = await self.repo.users.update(id=user.id, model=user)
        await self.repo.commit()
        return user

    async def update_user_phone(self, user: User) -> User:
        user: User = await self.repo.users.update(id=user.id, model=user)
        await self.repo.commit()
        return user

    async def delete_user_account(self, user: User) -> None:
        await self.repo.users.delete(id=user.id)
        await self.repo.commit()

    async def get_old_valid_refresh_token(self, user: User) -> RefreshToken:
        refresh_token: Optional[RefreshToken] = (
            await self.repo.refresh_tokens.get_user_valid_refresh_token(user_id=user.id)
        )
        if not refresh_token:
            raise RefreshTokenNotFound

        return refresh_token

    async def check_old_valid_refresh_token_existence(self, user: User) -> bool:
        refresh_token: Optional[RefreshToken] = (
            await self.repo.refresh_tokens.get_user_valid_refresh_token(user_id=user.id)
        )
        if refresh_token:
            return True

        return False

    async def get_all_managers_roles(self) -> List[UserRole]:
        return await self.repo.manager_roles.list()


class RedisAuthService:
    def __init__(self, cache: RedisRepository):
        self.cache = cache

    async def cache_user(self, user: User) -> None:
        user_dump: bytes = pickle.dumps(user)
        cache_data = CacheModel(
            key=settings.USER_PREFIX + str(user.id),
            value=str(user_dump),
            ttl=settings.USER_EXPIRATION_SECONDS,
        )
        await self.cache.set_data(cache_data)

    async def get_cached_user(self, user_id: int) -> Optional[User]:
        try:
            user_dump: bytes = await uow.cache.get(
                key=str(user_id), prefix=settings.USER_PREFIX
            )
            return pickle.loads(user_dump)
        except RedisKeyNotFound:
            pass

    async def delete_cached_user(self, user_id: int) -> None:
        await self.cache.delete(key=str(user_id), prefix=settings.USER_PREFIX)
