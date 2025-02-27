from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.company.dto import Contact, Address, Manager


@dataclass
class CompanyContext:
    inn: str
    ogrn: str
    kpp: str
    okpo: str
    registration_date: datetime
    legal_form:

    contacts: List[Contact]
    addresses: List[Address]
    management: List[Manager]