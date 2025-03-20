from src.auth.application.managers.auth_manager import AuthManager
from src.auth.presentation.api.router import router
from dependency_injector import inject
from fastapi import status, Depends

from src.auth.presentation.dependencies import get_auth_manager
from src.auth.presentation.schemas import RegisterUserScheme


@router.post("/register", status_code=status.HTTP_201_CREATED)
@inject
async def register(
    user_data: RegisterUserScheme,
    manager: AuthManager = Depends(get_auth_manager)
):
    user = await manager.register_user(user_data)
    # Отправка email...
    return user.to_dict()