from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from src.auth.application.services.auth_servcies import AuthService
from src.auth.application.services.user_services import (RedisUserService,
                                                         UserService)
from src.auth.config import auth_config
from src.auth.exceptions import (EmailAlreadyConfirmed, EmailNotConfirmed,
                                 EmailTaken, InvalidCredentials, PhoneTaken,
                                 UserNotFound)
from src.auth.infrastructure.models import RefreshToken, User
from src.auth.presentation.schemas import LoginUserScheme, RegisterUserScheme
from src.auth.security.password import check_password, hash_password
from src.core.utils import BasicCodeGenerator


class AuthManager:
    def __init__(
        self,
        auth_service: AuthService,
        user_service: UserService,
        redis_service: RedisUserService,
    ):
        self.auth = auth_service
        self.users = user_service
        self.cache = redis_service

    async def register_user(self, user_data: RegisterUserScheme) -> User:
        user: Optional[User] = None

        if await self.users.check_user_existence(email=user_data.email):
            user = await self.users.get_user_by_email(user_data.email)
            if user.is_email_confirmed:
                raise EmailTaken

        if await self.users.check_user_existence(phone=user_data.phone):
            if not (user and user.phone == user_data.phone):
                raise PhoneTaken

        if not user:
            new_user = User(**user_data.model_dump())
            new_user.password = hash_password(new_user.password)
            user = await self.users.register_user(new_user)
        else:
            user.password = hash_password(user_data.password)
            user = await self.users.update_user_profile(
                User(**(user.to_dict() | user_data.model_dump(exclude={"password"})))
            )
        return user

    async def login_user(self, auth_data: LoginUserScheme) -> User:
        try:
            user = await self.users.get_user_by_email(auth_data.email)
        except UserNotFound:
            raise InvalidCredentials

        if not user.is_email_confirmed:
            raise EmailNotConfirmed

        if not check_password(auth_data.password, user.password):
            raise InvalidCredentials

        return user

    async def authenticate_user(self, user_id: int) -> User:
        try:
            return await self.users.get_user_by_id(user_id)
        except UserNotFound:
            raise InvalidCredentials

    async def get_current_user(self, user_id: int) -> User:
        cached_user = await self.cache.get_cached_user(user_id)
        if cached_user:
            return cached_user

        user = await self.users.get_user_by_id(user_id)
        await self.cache.cache_user(user)
        return user

    async def verify_user_email(self, user: User) -> User:
        if user.is_email_confirmed:
            raise EmailAlreadyConfirmed

        verified_user = await self.users.verify_user_email(user)
        await self.cache.delete_cached_user(user.id)
        return verified_user

    async def create_refresh_token(self, user: User) -> RefreshToken:
        if await self.auth.check_old_valid_refresh_token_existence(user):
            old_token = await self.auth.get_old_valid_refresh_token(user)
            await self.auth.expire_refresh_token(old_token)

        new_token = RefreshToken(
            user_id=user.id,
            uuid=UUID(),
            refresh_token=BasicCodeGenerator.generate_random_alphanum(64),
            expires_at=datetime.utcnow()
            + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
        )

        return await self.auth.create_refresh_token(new_token)
