from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.company.dto import Contact, Address, Manager, FinancialReport, TaxReport, Translations
from src.company.enums import LegalStatus, SystemStatus


@dataclass
class RuCompanyContext:
    country_code: str
    legal_status: LegalStatus
    system_status: SystemStatus

    name: str
    legal_name: str
    inn: str
    ogrn: str
    kpp: str
    okpo: str
    registration_date: datetime
    legal_form: str
    authorized_capital: int
    average_number_of_employees: int

    okogu_code: str
    okopf_code: str
    okfs_code: str
    okato_code: str
    oktmo_code: str
    code_kladr: str

    contacts: List[Contact]
    addresses: List[Address]
    management: List[Manager]

    financial_reports: List[FinancialReport]
    tax_reports: List[TaxReport]

    translations: List[Translations]
