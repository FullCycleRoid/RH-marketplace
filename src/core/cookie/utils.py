import datetime
from fastapi import Response

from src.core.cookie.config import cookies_config


def set_cookie(response: Response, key: str, value: str, expire_days: int) -> Response:
    expires = datetime.datetime.utcnow() + datetime.timedelta(days=expire_days)
    response.set_cookie(
        key=key,
        value=value,
        secure=cookies_config.SECURE_COOKIES,
        expires=expires.strftime("%a, %d-%b-%Y %T GMT"),
        httponly=cookies_config.HTTP_ONLY,
        samesite=cookies_config.SAME_SITE
    )
    return response


def delete_cookie(response: Response, key: str):
    response.delete_cookie(key=key, secure=cookies_config.SECURE_COOKIES, httponly=cookies_config.HTTP_ONLY, samesite=cookies_config.SAME_SITE)
    return response
