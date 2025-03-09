from dataclasses import dataclass
from typing import Optional, List

from pydantic import Field


@dataclass
class OkvedNode:
    code: str
    description: str

    parent_node: Optional["OkvedNode"]
    child_nodes: Optional[List["OkvedNode"]] = Field(default_factory=list)


class OkvedContext:
    raw_codes: List[dict] = Field(default_factory=dict)
    okved_catalog: OkvedNode = Field(default_factory=list)
