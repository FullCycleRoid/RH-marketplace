from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


from src.core.constants import DB_NAMING_CONVENTION


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""
    metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

