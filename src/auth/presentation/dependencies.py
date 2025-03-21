from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from src.auth.application.managers.auth_manager import AuthManager
from src.auth.application.services.auth_servcies import AuthService
from src.auth.application.services.user_services import UserService
from src.auth.exceptions import UserNotFound
from src.auth.infrastructure.models import User
from src.core.containers import AuthContainer
from src.core.security.jwt import JWTData, parse_jwt_data_from_oauth2


def get_auth_manager(
    manager: AuthManager = Depends(Provide[AuthContainer.auth_manager]),
) -> AuthManager:
    return manager


def get_auth_service(
    service: AuthService = Depends(Provide[AuthContainer.auth_service]),
) -> AuthManager:
    return service


def get_user_service(
    service: UserService = Depends(Provide[AuthContainer.user_service]),
) -> UserService:
    return service


@inject
async def get_current_user(
    auth_manager: AuthManager = Depends(Provide[AuthContainer.auth_manager]),
    token_data: JWTData = Depends(parse_jwt_data_from_oauth2),
) -> User:
    try:
        return await auth_manager.authenticate_user(token_data.user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


CurrentUserDep = Annotated[User, Depends(get_current_user)]


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
AuthManagerDep = Annotated[AuthManager, Depends(get_auth_manager)]
