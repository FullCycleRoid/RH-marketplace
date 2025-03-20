from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.auth.application.managers.auth_manager import AuthManager
from src.core.containers import AuthContainer


def get_auth_manager(
    manager: AuthManager = Depends(Provide[AuthContainer.auth_manager]),
) -> AuthManager:
    return manager


AuthManagerDep = Annotated[AuthManager, Depends(get_auth_manager)]
