from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, text, BigInteger
from sqlalchemy.dialects.postgresql import JSONB, UUID

from src.core.database.metadata import metadata


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(100), nullable=False, unique=True),
    Column("password", String, nullable=False),
    Column("phone", String(20), nullable=False, unique=True),
    Column("is_email_confirmed", Boolean, default=False),
    Column("is_phone_number_confirmed", Boolean, default=False),

    Column("first_name", String(60), nullable=False, unique=False),
    Column("middle_name", String(60), nullable=True, unique=False),
    Column("last_name", String(60), nullable=True, unique=False),

    Column("manager_role_id", Integer, ForeignKey("manager_roles.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True),
    Column("telegram_username", String, nullable=True, unique=True),
    Column("telegram_id", BigInteger, nullable=True, unique=True),

    Column("created_at", DateTime, default=datetime.utcnow, server_default=text("TIMEZONE('utc', now())"), nullable=False),
    Column("updated_at", DateTime, default=datetime.utcnow, server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow, nullable=False)
)

manager_roles = Table(
    "manager_roles",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(40), nullable=False, unique=True),
    Column("permissions", JSONB, nullable=False)
)


refresh_tokens = Table(
    "refresh_tokens",
    metadata,
    Column("uuid", UUID, primary_key=True),
    Column("refresh_token", String, nullable=False),
    Column("expires_at", DateTime, nullable=False),

    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
    Column("created_time", DateTime, default=datetime.utcnow, server_default=text("TIMEZONE('utc', now())"), nullable=False),
    Column("updated_time", DateTime, default=datetime.utcnow, server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow, nullable=False)
)
