from abc import ABC
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional, Set


@dataclass
class BaseDTO(ABC):
    """
    Base model, from which any domain model should be inherited.
    """

    def to_dict(
        self,
        exclude: Optional[Set[str]] = None,
        include: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a dictionary representation of the model.

        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        data: Dict[str, Any] = asdict(self)

        if exclude:
            for key in exclude:
                try:
                    del data[key]
                except KeyError:
                    pass

        if include:
            data.update(include)

        return data

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}>"

    def __hash__(self) -> int:
        return hash(self.id)
