from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.company.enums import ContactType, ManagerType


@dataclass
class Contact:
    type: ContactType
    value: str
    is_verified: bool
    verified_at: bool


@dataclass
class Address:
    post_code: int
    region: str
    city: str
    street: str
    house: str
    full_address: str

    is_verified: bool


@dataclass
class Manager:
    position: ManagerType
    name: str
    patronymic: str
    surname: str
    inn: Optional[str]
    since_on_position: Optional[datetime]
