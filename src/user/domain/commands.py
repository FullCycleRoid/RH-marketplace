from dataclasses import dataclass

from src.core.interfaces.commands import AbstractCommand


@dataclass(frozen=True)
class SignUpCommand(AbstractCommand):
    pass
