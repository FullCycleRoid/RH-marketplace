from typing import List
from uuid import UUID

from pydantic import BaseModel

from src import Company


class CompanySerializer:
    @staticmethod
    def serialize(company: Company, lang: str = "RU") -> dict:
        ...

class CompanyResponseSchema(BaseModel):  # Для FastAPI/Starlette
    id: UUID
    name: str
    inn: str
    okveds: List[str]

    @classmethod
    def from_orm(cls, obj: Company):
        return cls(**CompanySerializer.serialize(obj))

