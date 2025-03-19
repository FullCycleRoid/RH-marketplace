import hashlib
from datetime import datetime, timedelta

from src.core.security.jwt import create_jwt_token
from src.user.config import auth_config
from src.user.models import User


def hash_password(password: str) -> str:
    hasher = hashlib.md5(bytes(password, "utf-8"))
    hashed_password = hasher.hexdigest()
    return hashed_password


def check_password(password: str, password_in_db: str) -> bool:
    hashed_password = hash_password(password)
    return hashed_password == password_in_db


def create_access_token(
    *,
    user: User,
    expires_delta: timedelta = timedelta(minutes=auth_config.ACCESS_TOKEN_EXP)
) -> str:

    jwt_data = {"sub": str(user.id), "exp": datetime.utcnow() + expires_delta}
    return create_jwt_token(jwt_data=jwt_data)


def create_verify_email_token(
    user: User,
    expires_delta: timedelta = timedelta(minutes=auth_config.VERIFY_EMAIL_JWT_EXP),
) -> str:

    jwt_data = {"sub": str(user.id), "exp": datetime.utcnow() + expires_delta}
    return create_jwt_token(jwt_data=jwt_data)


def create_forget_password_token(
    user: User,
    expires_delta: timedelta = timedelta(minutes=auth_config.FORGET_PASSWORD_JWT_EXP),
) -> str:

    jwt_data = {"sub": str(user.id), "exp": datetime.utcnow() + expires_delta}
    return create_jwt_token(jwt_data=jwt_data)
