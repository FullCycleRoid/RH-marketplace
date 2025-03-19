from typing import Any

from pydantic_settings import BaseSettings

from src.core.enums import Environment


class Config(BaseSettings):
    POOL_PRE_PING: bool = True
    POOL_RECYCLE: int = -1  # default to SQLAlchemy
    DB_ECHO: bool = False

    ENVIRONMENT: Environment = Environment.PRODUCTION

    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]
    APP_VERSION: str = "1"

    # DB Settings
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int
    MAX_POOL_CONNECTIONS: int

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # SMTP
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_LOGIN: str = ""
    SMTP_PASSWORD: str = ""
    FEEDBACK_SEND_TO: str = ""

    EMAIL_CODE_LENGTH: int = 6
    EMAIL_EXPIRATION_SECONDS: int = 3600
    CONFIRMATION_CODE_EXPIRATION_SECONDS: int = 180

    # Redis prefix
    EMAIL_CODE_PREFIX: str = "email_code:"

    USER_EXPIRATION_SECONDS: int = 24 * 60 * 60  # 1 day
    USER_PREFIX: str = "user:"


settings = Config()

app_configs: dict[str, Any] = {"title": "RH API"}

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
