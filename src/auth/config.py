from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 5  # minutes
    VERIFY_EMAIL_JWT_EXP: int = 60 * 24 * 365  # 1 year
    FORGET_PASSWORD_JWT_EXP: int = 60 * 24  # 1 day

    REFRESH_TOKEN_KEY: str = "refreshToken"
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days

    ACCESS_TOKEN_KEY: str = "accessToken"
    ACCESS_TOKEN_EXP: int = 60 * 60 * 24  # 24 hour

    SECURE_COOKIES: bool = True
    HTTP_ONLY: bool = False
    SAME_SITE: str = "None"


auth_config = AuthConfig()
