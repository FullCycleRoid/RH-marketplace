import random
import smtplib
import string
from datetime import datetime, timedelta
from os import walk
from typing import List

from pydantic import EmailStr

from src.config import settings
from src.core.constants import DatetimeFormats
from src.core.enums import EnvRedirectUrlsEnum


class BasicCodeGenerator:
    @classmethod
    def get_code(cls, length: int = 6, numeric: bool = True) -> str:
        if numeric:
            return cls._generate_numeric_code(length=length)
        return cls._generate_upper_characters_code(length=length)

    @classmethod
    def generate_random_alphanum(cls, length: int = 20) -> str:
        return cls._generate_alphanum(length=length)

    @staticmethod
    def _generate_numeric_code(length: int = 6) -> str:
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def _generate_upper_characters_code(length: int = 6) -> str:
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @staticmethod
    def _generate_alphanum(length: int = 20) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))


# TODO move to class all redirect URLS
def choose_env_redirect_url(redirect_type: str = EnvRedirectUrlsEnum.AUTO_CP) -> str:
    match redirect_type:
        case EnvRedirectUrlsEnum.AUTO_CP:
            return choose_auto_cp_redirect_url()
        case EnvRedirectUrlsEnum.SHORT_AUTO_CP:
            return choose_short_auto_cp_redirect_url()
        case EnvRedirectUrlsEnum.VERIFY_EMAIL:
            return choose_verify_email_redirect_url()
        case EnvRedirectUrlsEnum.FORGET_PASSWORD:
            return choose_forget_password_redirect_url()


def choose_auto_cp_redirect_url() -> str:
    if settings.ENVIRONMENT.is_deployed:
        return settings.PROD_AUTO_CP_REDIRECT_URL
    else:
        return settings.DEV_AUTO_CP_REDIRECT_URL


def choose_short_auto_cp_redirect_url() -> str:
    if settings.ENVIRONMENT.is_deployed:
        return settings.PROD_SHORT_AUTO_CP_REDIRECT_URL
    else:
        return settings.DEV_SHORT_AUTO_CP_REDIRECT_URL


def choose_verify_email_redirect_url() -> str:
    if settings.ENVIRONMENT.is_deployed:
        return settings.PROD_VERIFY_EMAIL_REDIRECT_URL
    elif settings.ENVIRONMENT.is_local:
        return "http://0.0.0.0:8000/marketplace/auth/users/verify_email/"
    else:
        return settings.DEV_VERIFY_EMAIL_REDIRECT_URL


def choose_forget_password_redirect_url() -> str:
    if settings.ENVIRONMENT.is_deployed:
        return settings.PROD_FORGET_PASSWORD_REDIRECT_URL
    elif settings.ENVIRONMENT.is_local:
        return "http://0.0.0.0:8000/marketplace/auth/users/new_password/"
    else:
        return settings.DEV_FORGET_PASSWORD_REDIRECT_URL


def build_full_paths_for_all_files_in_a_folder(folder_path: str) -> List[str]:
    files_path = []
    for _, _, filenames in walk("/src/src/core/cache/dumps/gesn_catalog/"):
        for filename in filenames:
            files_path.append(folder_path + filename)

    return files_path


def current_base_url_domain() -> str:
    if settings.ENVIRONMENT.is_deployed:
        return "https://21yard.com"
    else:
        return "https://dev.21yard.com"


def __send_email(email_to: EmailStr, message_content: str):
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_LOGIN, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_LOGIN, email_to, message_content)


def transform_datetime_format(
    to_transform: datetime, datetime_format: str = DatetimeFormats.RUSSIAN
) -> str:
    return to_transform.strftime(datetime_format)


def datetime_until(days: int) -> datetime:
    return datetime.today() + timedelta(days=days)
