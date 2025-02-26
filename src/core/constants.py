from typing import Tuple, Any, Dict
from dataclasses import astuple, dataclass


DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


@dataclass(frozen=True)
class BaseConstant:

    def to_tuple(self) -> Tuple[Any, ...]:
        return astuple(self)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


class ErrorCode:
    ACCEPT_CODE_NOT_FOUND = "Код подтверждения не найден"
    WRONG_ACCEPT_CODE = "Неверный код подтверждения"
    REDIS_KEY_NOT_FOUND = "Ключ Redis не найден"


@dataclass(frozen=True)
class DatetimeFormats:
    RUSSIAN: str = '%d.%m.%Y %H:%M:%S'
