from datetime import datetime, timedelta
from typing import Callable

from src.auth.config import auth_config
from src.auth.infrastructure.models import User
from src.core.security.jwt import create_jwt_token


def _generate_token_data(user: User, expires_delta: timedelta) -> dict:
    return {"sub": str(user.id), "exp": datetime.utcnow() + expires_delta}


def create_token_generator(
    default_expires_delta: timedelta,
    custom_payload: Callable[[User, dict], None] = None,
) -> Callable[[User, timedelta], str]:
    def generate_token(
        user: User, expires_delta: timedelta = default_expires_delta
    ) -> str:
        token_data = _generate_token_data(user, expires_delta)
        if custom_payload:
            custom_payload(user, token_data)
        return create_jwt_token(jwt_data=token_data)

    return generate_token


create_access_token = create_token_generator(
    default_expires_delta=timedelta(minutes=auth_config.ACCESS_TOKEN_EXP)
)

create_verify_email_token = create_token_generator(
    default_expires_delta=timedelta(minutes=auth_config.VERIFY_EMAIL_JWT_EXP)
)

create_forget_password_token = create_token_generator(
    default_expires_delta=timedelta(minutes=auth_config.FORGET_PASSWORD_JWT_EXP)
)
