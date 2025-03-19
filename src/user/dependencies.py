import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends
from pydantic import EmailStr

from src.config import settings
from src.core.cache.redis.units_of_work import RedisUnitOfWork
from src.core.security.jwt import (
    oauth2_scheme,
    parse_jwt_data_from_oauth2,
    parse_jwt_data_from_token,
    refresh_token_scheme,
)
from src.core.utils import BasicCodeGenerator
from src.user.config import auth_config
from src.user.exceptions import (
    EmailAlreadyConfirmed,
    EmailNotConfirmed,
    EmailTaken,
    ExpiredToken,
    IncorrectOldPassword,
    InvalidCredentials,
    InvalidToken,
    PhoneTaken,
    RefreshTokenNotValid,
    UserNotFound,
    UserPhoneAlreadyVerified,
)
from src.user.models import RefreshToken, User
from src.user.schemas import (
    ChangeForgottenPasswordScheme,
    ChangeOldPasswordScheme,
    JWTData,
    LoginUserScheme,
    RegisterUserScheme,
    UpdateUserPhoneScheme,
    UpdateUserProfileScheme,
)
from src.user.security import check_password, hash_password
from src.user.service import AuthService, RedisAuthService
from src.user.units_of_work import SQLAlchemyUsersUnitOfWork
from src.user.views import AuthViews


async def register_user(user_data: RegisterUserScheme) -> User:
    user: Optional[User] = None
    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    if await auth_service.check_user_existence(email=user_data.email):
        user = await auth_service.get_user_by_email(email=user_data.email)
        if user.is_email_confirmed:
            raise EmailTaken

    if await auth_service.check_user_existence(phone=user_data.phone):
        if not (user and user.phone == user_data.phone):
            raise PhoneTaken

    if not user:
        new_user: User = User(**user_data.model_dump())
        new_user.password = hash_password(new_user.password)
        user = await auth_service.register_user(user=new_user)
    else:
        user.password = hash_password(user_data.password)
        user = await auth_service.update_user_profile(
            user=User(**(user.to_dict() | user_data.model_dump(exclude={"password"})))
        )

    return user


async def login_user(auth_data: LoginUserScheme) -> User:
    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    user: User = await auth_service.get_user_by_email(email=auth_data.email)
    if not user:
        raise UserNotFound

    if not user.is_email_confirmed:
        raise EmailNotConfirmed

    if not check_password(password=auth_data.password, password_in_db=user.password):
        raise InvalidCredentials

    return user


async def authenticate_user(
    jwt_data: JWTData = Depends(parse_jwt_data_from_oauth2),
) -> User:
    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    user: User = await auth_service.get_user_by_id(jwt_data.user_id)
    if not user:
        raise UserNotFound

    return user


async def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_data_from_oauth2),
) -> User:
    cache_service: RedisAuthService = RedisAuthService(uow=RedisUnitOfWork())
    user: Optional[User] = await cache_service.get_cached_user(user_id=jwt_data.user_id)

    if not user:
        auth_views: AuthViews = AuthViews(uow=SQLAlchemyUsersUnitOfWork())
        user = await auth_views.get_user_by_id(user_id=jwt_data.user_id)
        await cache_service.cache_user(user=user)

    return user


async def get_user_by_token(
    jwt_data: JWTData = Depends(parse_jwt_data_from_token),
) -> User:
    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    user: User = await auth_service.get_user_by_id(jwt_data.user_id)
    if not user:
        raise UserNotFound

    return user


async def verify_user_email(user: User = Depends(get_user_by_token)) -> User:
    if user.is_email_confirmed:
        raise EmailAlreadyConfirmed

    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    user = await auth_service.verify_user_email(user=user)

    cache_service: RedisAuthService = RedisAuthService(uow=RedisUnitOfWork())
    await cache_service.delete_cached_user(user_id=user.id)
    return user


async def valid_user_email(email: EmailStr) -> User:
    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    user: User = await auth_service.get_user_by_email(email=email)
    if not user:
        raise UserNotFound

    return user


async def create_refresh_token(user: User) -> RefreshToken:
    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())

    # Only one valid refresh token should exist at the moment of time:
    if await auth_service.check_old_valid_refresh_token_existence(user=user):
        old_valid_refresh_token: RefreshToken = (
            await auth_service.get_old_valid_refresh_token(user=user)
        )
        await auth_service.expire_refresh_token(refresh_token=old_valid_refresh_token)

    new_refresh_token: RefreshToken = await auth_service.create_refresh_token(
        RefreshToken(
            user_id=user.id,
            uuid=uuid.uuid4(),
            refresh_token=BasicCodeGenerator.generate_random_alphanum(64),
            expires_at=datetime.utcnow()
            + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
        )
    )
    logging.info(
        f"Created refresh token {new_refresh_token.refresh_token}, which will expire at {new_refresh_token.expires_at}"
    )

    return new_refresh_token


async def valid_refresh_token(
    refresh_token_value: Optional[str] = Depends(refresh_token_scheme),
) -> RefreshToken:
    if not refresh_token_value:
        raise RefreshTokenNotValid

    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    refresh_token: RefreshToken = await auth_service.get_refresh_token_by_value(
        value=refresh_token_value
    )
    if not refresh_token:
        logging.info(f"Provided refresh-token {refresh_token_value} was not found")
        raise RefreshTokenNotValid

    if not datetime.utcnow() <= refresh_token.expires_at:
        logging.info(
            f"Refresh-token {refresh_token.refresh_token} expires at {refresh_token.expires_at}, "
            f"current time: {datetime.utcnow()}"
        )
        raise RefreshTokenNotValid

    return refresh_token


async def get_user_by_refresh_token(
    refresh_token: RefreshToken = Depends(valid_refresh_token),
) -> User:
    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    user: User = await auth_service.get_user_by_id(refresh_token.user_id)
    if not user:
        raise UserNotFound

    return user


async def expire_refresh_token(
    refresh_token_value: Optional[str] = Depends(refresh_token_scheme),
) -> Optional[RefreshToken]:
    if not refresh_token_value:
        return

    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    if await auth_service.check_refresh_token_existence(value=refresh_token_value):
        refresh_token: RefreshToken = await auth_service.get_refresh_token_by_value(
            value=refresh_token_value
        )
        return await auth_service.expire_refresh_token(refresh_token)


async def change_forgotten_password(
    password_data: ChangeForgottenPasswordScheme,
    user: User = Depends(get_user_by_token),
) -> User:

    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    user.password = hash_password(password_data.new_password)
    user = await auth_service.update_user_profile(user=user)

    cache_service: RedisAuthService = RedisAuthService(uow=RedisUnitOfWork())
    await cache_service.delete_cached_user(user_id=user.id)

    return user


async def validate_access_token(token: Optional[str] = Depends(oauth2_scheme)) -> bool:
    if not token:
        return False

    try:
        jwt_data: JWTData = await parse_jwt_data_from_token(token=token)
    except (ExpiredToken, InvalidToken):
        return False

    if jwt_data.expires.astimezone(tz=timezone.utc) < (
        datetime.now(tz=timezone.utc) + timedelta(seconds=30)
    ):
        return False

    return True


async def update_user_profile(
    update_user_data: UpdateUserProfileScheme, user: User = Depends(authenticate_user)
) -> User:

    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    updated_user: User = User(
        **(user.to_dict() | update_user_data.model_dump(exclude_unset=True))
    )
    user = await auth_service.update_user_profile(user=updated_user)

    cache_service: RedisAuthService = RedisAuthService(uow=RedisUnitOfWork())
    await cache_service.delete_cached_user(user_id=user.id)
    return user


async def update_user_phone(
    update_phone_data: UpdateUserPhoneScheme, user: User = Depends(authenticate_user)
) -> User:

    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    if user.is_phone_number_confirmed:
        raise UserPhoneAlreadyVerified

    updated_user: User = User(
        **(user.to_dict() | update_phone_data.model_dump(exclude_unset=True))
    )
    user = await auth_service.update_user_phone(user=updated_user)

    cache_service: RedisAuthService = RedisAuthService(uow=RedisUnitOfWork())
    await cache_service.delete_cached_user(user_id=user.id)
    return user


async def change_old_password(
    password_data: ChangeOldPasswordScheme, user: User = Depends(authenticate_user)
) -> User:

    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    if not check_password(
        password=password_data.old_password, password_in_db=user.password
    ):
        raise IncorrectOldPassword

    user.password = hash_password(password_data.new_password)
    user = await auth_service.update_user_profile(user=user)

    cache_service: RedisAuthService = RedisAuthService(uow=RedisUnitOfWork())
    await cache_service.delete_cached_user(user_id=user.id)

    return user


async def delete_my_account(user: User = Depends(authenticate_user)) -> None:
    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    await auth_service.delete_user_account(user=user)

    cache_service: RedisAuthService = RedisAuthService(uow=RedisUnitOfWork())
    await cache_service.delete_cached_user(user_id=user.id)
