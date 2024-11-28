from pydantic_settings import BaseSettings


class CookiesConfig(BaseSettings):
    TOKEN_COOKIES_KEY: str = "Access-Token"
    DEMO_CP_COOKIE_KEY: str = "DemoID"
    COOKIES_LIFESPAN: int = 31  # 1 month according legacy backend cookies lifespan
    SECURE_COOKIES: bool = False
    HTTP_ONLY: bool = False
    SAME_SITE: str = "Lax"
    DOMAIN: str = "russian-house.ru"


cookies_config = CookiesConfig()
