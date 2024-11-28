from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import JSON, String, Boolean, ForeignKey, DateTime, func, Integer, BIGINT

from src.core.database.base import Base


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    inn: Mapped[str] = mapped_column(nullable=False, unique=True)
    ogrn: Mapped[str] = mapped_column(nullable=True, unique=True)
    kpp: Mapped[str]
    okpo: Mapped[str]

    registration_timestamp: Mapped[BIGINT]

    okogu: Mapped[str]
    okopf: Mapped[str]
    okfs: Mapped[str]
    okato: Mapped[str]
    oktmo: Mapped[str]
    kladr: Mapped[str]

    authorized_capital: Mapped[int]

    quantity_employees: Mapped[int]

    # director_fio: Mapped[str]
    # director_since: Mapped[str]

    sanctions: Mapped[str]
    advantages: Mapped[str]

    # faxes_profile: Mapped[str]
    # financial_profile: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),  nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)

    # name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    # description: Mapped[str]
    #
    # legal_name: Mapped[str] = mapped_column(String, unique=True)
    # legal_form: Mapped[str]
    # legal_state: Mapped[str]
    # legal_address: Mapped[str]
    # legal_description: Mapped[str]


class CompanyLocalization(Base):
    __tablename__ = "company_translation"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    lang_key: Mapped[str]
    field_name: Mapped[str]
    value: Mapped[str]


class Management(Base):
    __tablename__ = "management"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    role: Mapped[str]  # Director Manager


class ManagementLocalization(Base):
    __tablename__ = "management_localization"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    management_id: Mapped[int] = mapped_column(Integer, ForeignKey("management.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    lang_key: Mapped[str] #  EN         Ru
    role: Mapped[str]  #     Director   Директор
    first_name: Mapped[str]
    middle_name: Mapped[str]
    lastname_name: Mapped[str]


class FinancialProfile(Base):
    pass

class TaxesProfile(Base):
    pass



class CompanyContacts(Base):
    __tablename__ = "company_contacts"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    type: Mapped[str]  # EMAIL, PHONE, TELEGRAM, SOCIAL, WEBSITE, INSTAGRAM, WHATSAPP, VK, YOUTUBE
    data: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),  nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)


class CompanyOKVEDContacts(Base):
    __tablename__ = "company_okved_m2m"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    okved_id: Mapped[int] = mapped_column(Integer, ForeignKey("okved.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    state: Mapped[str]  # MAIN, SECONDARY

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),  nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)


class OKVED(Base):
    __tablename__ = "okved"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    code: Mapped[str]
    name: Mapped[str]
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("okved.id"))
