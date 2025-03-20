import re

from email_validator import validate_email
from email_validator.exceptions_types import EmailSyntaxError

from src.auth.exceptions import EmailNotValid


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
