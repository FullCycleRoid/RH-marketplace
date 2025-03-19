from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship

from src.core.database.declarative_base import Base


class Dialogue(Base):
    __tablename__ = "dialogues"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_a_id = Column(UUID, ForeignKey("companies.id"))
    company_b_id = Column(UUID, ForeignKey("companies.id"))

    company_a = relationship("Company", foreign_keys=[company_a_id])
    company_b = relationship("Company", foreign_keys=[company_b_id])
    messages = relationship("Message", back_populates="dialogue")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    timestamp = Column(DateTime, default=func.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    dialogue_id = Column(UUID, ForeignKey("dialogues.id"))

    # user = relationship("User", back_populates="messages")
    dialogue = relationship("Dialogue", back_populates="messages")
