from pydantic_settings import BaseSettings


class CookiesConfig(BaseSettings):
    TOKEN_COOKIES_KEY: str = "Access-Token"
    COOKIES_LIFESPAN: int = 31
    SECURE_COOKIES: bool = False
    HTTP_ONLY: bool = True
    SAME_SITE: str = "Lax"


cookies_config = CookiesConfig()
