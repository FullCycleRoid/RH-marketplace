import re
from typing import Any

from email_validator import validate_email
from email_validator.exceptions_types import EmailSyntaxError

from src.auth.config import auth_config
from src.user.exceptions import EmailNotValid


def get_cookie_settings(
    key: str, value: str, max_age: int = 0, expired: bool = False
) -> dict[str, Any]:

    base_cookie = {
        "key": key,
        "httponly": auth_config.HTTP_ONLY,
        "samesite": auth_config.SAME_SITE,
        "secure": auth_config.SECURE_COOKIES,
    }
    if expired:
        return base_cookie

    return {**base_cookie, "value": value, "max_age": max_age}


def validate_email_or_raise_error(email: str):
    try:
        return validate_email(email).normalized
    except EmailSyntaxError:
        raise EmailNotValid


def validate_phone_number(phone: str):
    for symbol in ("-", "(", ")", " "):
        phone = phone.replace(symbol, "")

    pattern = re.compile(r"^\+?[78]-?\s?[-\(]?\d{3}\)?-?\s?\d{3}-?\s?\d{2}-?\s?\d{2}$")
    data = pattern.search(phone)
    if not data:
        raise ValueError("Некорректный номер мобильного телефона")

    return phone
