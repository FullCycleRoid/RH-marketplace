# routes.py
from containers import AuthContainer
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
@inject
async def register(
    user_data: RegisterUserScheme,
    manager: AuthManager = Depends(Provide[AuthContainer.auth_manager]),
):
    user = await manager.register_user(user_data)
    # Отправка email...
    return user.to_dict()


@router.post("/login")
@inject
async def login(
    auth_data: LoginUserScheme,
    manager: AuthManager = Depends(Provide[AuthContainer.auth_manager]),
):
    user = await manager.login_user(auth_data)
    # Генерация токенов...
    return user.to_dict()


@router.get("/me")
@inject
async def get_me(
    manager: AuthManager = Depends(Provide[AuthContainer.auth_manager]),
    user: User = Depends(get_current_user_dependency),
):
    return user.to_dict()


@router.patch("/verify-email")
@inject
async def verify_email(
    manager: AuthManager = Depends(Provide[AuthContainer.auth_manager]),
    user: User = Depends(get_user_by_token),
):
    verified_user = await manager.verify_user_email(user)
    return verified_user.to_dict()


# Остальные роутеры аналогично...
