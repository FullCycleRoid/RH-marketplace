import pickle
from typing import List, Optional

from src.auth.exceptions import UserNotFound
from src.auth.infrastructure.models import User, UserRole
from src.auth.infrastructure.repositories.postgres import \
    SQLAlchemyUsersRepository
from src.core.cache.redis.DTO import CacheModel
from src.core.cache.redis.repositories import RedisRepository
from src.core.config.config import settings
from src.core.exceptions import RedisKeyNotFound


class UserService:
    def __init__(self, user_repository: SQLAlchemyUsersRepository) -> None:
        self.user_repository = user_repository

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
            user = await self.user_repository.users.get(id=id)
            if user:
                return True

        if email:
            user = await self.user_repository.users.get_by_email(email)
            if user:
                return True

        if phone:
            user = await self.user_repository.users.get_by_phone(phone)
            if user:
                return True

        if telegram_username:
            user = await self.user_repository.users.get_by_telegram_username(
                telegram_username
            )
            if user:
                return True

        if telegram_id:
            user = await self.user_repository.users.get_by_telegram_id(telegram_id)
            if user:
                return True

        return False

    async def register_user(self, user: User) -> User:
        user: User = await self.user_repository.users.add(user)
        await self.user_repository.commit()
        return user

    async def verify_user_email(self, user: User) -> User:
        user.is_email_confirmed = True
        user: User = await self.user_repository.users.update(id=user.id, model=user)
        await self.user_repository.commit()
        return user

    async def get_user_by_id(self, id: int) -> User:
        user: Optional[User] = await self.user_repository.users.get(id=id)
        if not user:
            raise UserNotFound

        return user

    async def get_user_by_email(self, email: str) -> User:
        user: Optional[User] = await self.user_repository.users.get_by_email(
            email=email
        )
        if not user:
            raise UserNotFound

        return user

    async def get_user_by_optional_email(self, email: str) -> Optional[User]:
        return await self.user_repository.users.get_by_email(email=email)

    async def get_user_by_phone(self, phone: str) -> User:
        user: Optional[User] = await self.user_repository.users.get_by_phone(
            phone=phone
        )
        if not user:
            raise UserNotFound

        return user

    async def update_user_profile(self, user: User) -> User:
        user: User = await self.user_repository.users.update(id=user.id, model=user)
        await self.user_repository.commit()
        return user

    async def update_user_phone(self, user: User) -> User:
        user: User = await self.user_repository.users.update(id=user.id, model=user)
        await self.user_repository.commit()
        return user

    async def delete_user_account(self, user: User) -> None:
        await self.user_repository.users.delete(id=user.id)
        await self.user_repository.commit()

    async def get_all_managers_roles(self) -> List[UserRole]:
        return await self.user_repository.manager_roles.list()


class RedisUserService:
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
            user_dump: bytes = await self.cache.get(
                key=str(user_id), prefix=settings.USER_PREFIX
            )
            return pickle.loads(user_dump)
        except RedisKeyNotFound:
            pass

    async def delete_cached_user(self, user_id: int) -> None:
        await self.cache.delete(key=str(user_id), prefix=settings.USER_PREFIX)
