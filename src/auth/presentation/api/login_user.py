from dependency_injector import inject
from fastapi import Depends, Response, status

from src.auth.application.managers.auth_manager import AuthManager
from src.auth.application.services.depends_scratch import create_refresh_token
from src.auth.config import auth_config, get_cookie_settings
from src.auth.infrastructure.models import RefreshToken, User
from src.auth.presentation.api.router import router
from src.auth.presentation.dependencies import get_auth_manager
from src.auth.presentation.schemas import LoginUserScheme
from src.auth.security.tokens import create_access_token


@router.post("/login", status_code=status.HTTP_200_OK)
@inject
async def login(
    response: Response,
    auth_data: LoginUserScheme,
    manager: AuthManager = Depends(get_auth_manager),
):
    user = await manager.login_user(auth_data)

    refresh_token: RefreshToken = await create_refresh_token(user=user)
    response.set_cookie(
        **get_cookie_settings(
            key=auth_config.REFRESH_TOKEN_KEY,
            value=refresh_token.refresh_token,
            max_age=auth_config.REFRESH_TOKEN_EXP,
        )
    )

    response.set_cookie(
        **get_cookie_settings(
            key=auth_config.ACCESS_TOKEN_KEY,
            value=create_access_token(user=user),
            max_age=auth_config.ACCESS_TOKEN_EXP,
        )
    )

    return user.to_dict()
