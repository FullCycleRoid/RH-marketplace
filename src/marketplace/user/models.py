from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import JSON, String, Boolean, ForeignKey, DateTime, func, Integer

from src.core.database.postgres import Base


class UserRole(Base):
    __tablename__ = "user_role"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    permissions: Mapped[JSON] = mapped_column(type_=JSON)


class User(Base):
    __tablename__ = "user"

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)
    # -------------------------

    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_role.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)

    telegram_username: Mapped[str] = mapped_column(String(60), nullable=True, unique=True)
    telegram_id: Mapped[str] = mapped_column(String(60), nullable=True, unique=True)

    first_name: Mapped[str] = mapped_column(String(60), nullable=True)
    middle_name: Mapped[str] = mapped_column(String(60), nullable=True)
    last_name: Mapped[str] = mapped_column(String(60), nullable=True)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)


    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)

    phone: Mapped[str] = mapped_column(String(20))
    password: Mapped[str]

    is_email_confirm: Mapped[bool] = mapped_column(Boolean, default=False)
    is_phone_number_confirm: Mapped[bool] = mapped_column(Boolean, default=False)


class CompanyUserM2M(Base):
    __tablename__ = "company_user_m2m"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),  nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str]

    legal_name: Mapped[str] = mapped_column(String, unique=True)
    legal_form: Mapped[str]
    legal_state: Mapped[str]
    legal_address: Mapped[str]
    legal_description: Mapped[str]  # from checko

    inn: Mapped[str] = mapped_column(nullable=False, unique=True)
    ogrn: Mapped[str] = mapped_column(nullable=True, unique=True)
    kpp: Mapped[str]
    okpo: Mapped[str]
    registration_date: Mapped[str]

    authorized_capital: Mapped[str]

    director_fio: Mapped[str]
    director_since: Mapped[str]

    quantity_employees: Mapped[str]

    sanctions: Mapped[str]
    advantages: Mapped[str]

    okogu: Mapped[str]
    okopf: Mapped[str]
    okfs: Mapped[str]
    okato: Mapped[str]
    oktmo: Mapped[str]
    kladr: Mapped[str]

    # m2m okveds

    faxes_profile: Mapped[str]
    financial_profile: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),  nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)


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
