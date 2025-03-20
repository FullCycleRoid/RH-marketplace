from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from src.core.interfaces.dto import BaseDTO


@dataclass
class CacheModel(BaseDTO):
    key: bytes | str
    value: bytes | str
    ttl: Optional[int | timedelta] = None
