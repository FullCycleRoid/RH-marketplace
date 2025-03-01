from sqlalchemy import (Column, Integer, ForeignKey, DateTime, Text, func)
from sqlalchemy.orm import relationship

from src.core.database.declarative_base import Base


class Dialogue(Base):
    __tablename__ = "dialogues"
    id = Column(Integer, primary_key=True, index=True)
    company_a_id = Column(Integer, ForeignKey("companies.id"))
    company_b_id = Column(Integer, ForeignKey("companies.id"))

    company_a = relationship("Company", foreign_keys=[company_a_id])
    company_b = relationship("Company", foreign_keys=[company_b_id])
    messages = relationship("Message", back_populates="dialogue")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    timestamp = Column(DateTime, default=func.now)
    manager_id = Column(Integer, ForeignKey("managers.id"))
    dialogue_id = Column(Integer, ForeignKey("dialogues.id"))

    manager = relationship("Manager", back_populates="messages")
    dialogue = relationship("Dialogue", back_populates="messages")