from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.core.database.declarative_base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    uuid = Column(UUID, primary_key=True)
    refresh_token = Column(String, nullable=False)

    expires_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_time = Column(DateTime(timezone=True), onupdate=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())
