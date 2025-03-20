from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.auth.enums import ActiveState, AuthProvider, CreationMethod
from src.core.database.declarative_base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255))  # Может быть NULL для OAuth пользователей
    first_name = Column(String(255))
    last_name = Column(String(255))
    provider = Column(Enum(AuthProvider), nullable=False, default=AuthProvider.EMAIL)
    provider_user_id = Column(String(255))  # ID пользователя в системе провайдера

    company_id = Column(Integer)
    role_id = Column(Integer, ForeignKey("user_role.id"))

    active_state = Column(
        Enum(ActiveState, name="activestate", create_type=True),
        nullable=False,
        default=ActiveState.WAIT_FOR_VERIFICATION,
    )
    creation_method = Column(
        Enum(CreationMethod, name="creationmethod", create_type=True),
        nullable=False,
        default=CreationMethod.REGISTERED,
    )
    is_email_verified = Column(Boolean, nullable=False, default=False)
    is_phone_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    role = relationship("UserRole", back_populates="user")
    # messages = relationship("Message", back_populates="messages")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', provider='{self.provider}')>"


class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    permissions = Column(JSONB, nullable=False)

    user = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}>"


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    uuid = Column(UUID, primary_key=True)
    refresh_token = Column(String, nullable=False)

    expires_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_time = Column(DateTime(timezone=True), onupdate=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())
