from typing import Any, Dict, Optional, Set, TypeVar

from sqlalchemy.orm import DeclarativeBase

BaseMT = TypeVar('BaseMT', bound='Base')


class Base(DeclarativeBase):
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
        data: Dict[str, Any] = {
            c.name: getattr(self, c.name) for c in self.__table__.columns
        }

        if exclude:
            for key in exclude:
                try:
                    del data[key]
                except KeyError:
                    pass

        if include:
            data.update(include)

        return data
