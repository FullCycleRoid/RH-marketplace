from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from src.core.interfaces import BaseModel


@dataclass
class CacheModel(BaseModel):
    key: bytes | str
    value: bytes | str
    ttl: Optional[int | timedelta] = None
