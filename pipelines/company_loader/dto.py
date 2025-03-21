from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.company.enums import AddressType, ContactType, EntityType, ManagerType


@dataclass
class Contact:
    type: ContactType
    value: str
    is_verified: bool


@dataclass
class Address:
    type: AddressType
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
    full_name: str
    en_full_name: str

    since_on_position: Optional[datetime]
    inn: Optional[str] = None


@dataclass
class FinancialReport:
    year: datetime
    annual_income: int
    net_profit: int
    currency: str


@dataclass
class TaxReport:
    year: datetime
    taxes_paid: int
    paid_insurance: int


@dataclass
class Translations:
    entity_id: UUID
    entity_type: EntityType
    field_name: str
    language_code: str
    value: str
