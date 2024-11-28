from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import JSON, String, Boolean, ForeignKey, DateTime, func, Integer

from src.core.database.base import Base


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
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_role.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),  nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=datetime.utcnow, nullable=False)
