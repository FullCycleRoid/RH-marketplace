from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.company.enums import ContactType, ManagerType, AddressType, ReportStatus, EntityType


@dataclass
class Contact:
    type: ContactType
    value: str
    is_verified: bool
    verified_at: bool


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
    name: str
    patronymic: str
    surname: str
    inn: Optional[str]
    since_on_position: Optional[datetime]


@dataclass
class FinancialReport:
    year: datetime
    annual_income: int
    net_profit: int
    currency: str


@dataclass
class TaxReport:
    year: datetime
    quarter: str
    period_start: datetime
    period_end: datetime
    status: ReportStatus


@dataclass
class Translations:
    entity_id: UUID
    entity_type: EntityType
    field_name: str
    language_code: str
    value: str
