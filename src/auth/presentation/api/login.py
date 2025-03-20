from fastapi import Depends, Response, status

from src.auth.config import auth_config
from src.auth.infrastructure.models import RefreshToken, User
from src.auth.presentation.api.router import router
from src.auth.security import create_access_token
from src.auth.validators import get_cookie_settings


@router.post("/tokens", status_code=status.HTTP_200_OK, response_model=None)
async def login(response: Response, user: User = Depends(login_user)):
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
