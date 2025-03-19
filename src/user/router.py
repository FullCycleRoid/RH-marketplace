from fastapi import APIRouter, Depends, Response, status

from src.tasks.tasks import send_forget_password_email, send_verify_email_message
from src.user.config import auth_config
from src.user.dependencies import change_forgotten_password
from src.user.dependencies import change_old_password as change_old_password_dependency
from src.user.dependencies import create_refresh_token
from src.user.dependencies import delete_my_account as delete_my_account_dependency
from src.user.dependencies import get_my_account as get_my_account_dependency
from src.user.dependencies import get_user_by_refresh_token, login_user, register_user
from src.user.dependencies import update_user_phone as update_user_phone_dependency
from src.user.dependencies import update_user_profile as update_user_profile_dependency
from src.user.dependencies import valid_user_email
from src.user.dependencies import (
    validate_access_token as validate_access_token_dependency,
)
from src.user.dependencies import verify_user_email
from src.user.models import RefreshToken, User
from src.user.security import (
    create_access_token,
    create_forget_password_token,
    create_verify_email_token,
)
from src.user.utils import get_cookie_settings

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def register(user: User = Depends(register_user)):
    send_verify_email_message.delay(
        token=create_verify_email_token(user=user), email_to=user.email
    )

    return user.to_dict()


@router.get("/me", status_code=status.HTTP_200_OK, response_model=None)
async def get_my_account(user: User = Depends(get_my_account_dependency)):
    return user.to_dict()


@router.get(
    "/verify-email/{token}", status_code=status.HTTP_200_OK, response_model=None
)
async def verify_email(response: Response, user: User = Depends(verify_user_email)):
    await login(response=response, user=user)
    return user.to_dict()


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


@router.put("/tokens", status_code=status.HTTP_200_OK, response_model=None)
async def refresh_access_token(
    response: Response, user: User = Depends(get_user_by_refresh_token)
):
    response.set_cookie(
        **get_cookie_settings(
            key=auth_config.ACCESS_TOKEN_KEY,
            value=create_access_token(user=user),
            max_age=auth_config.ACCESS_TOKEN_EXP,
        )
    )


@router.delete("/tokens", status_code=status.HTTP_200_OK, response_model=None)
async def logout(response: Response):
    response.delete_cookie(
        **get_cookie_settings(key=auth_config.ACCESS_TOKEN_KEY, value="", expired=True)
    )

    response.delete_cookie(
        **get_cookie_settings(key=auth_config.REFRESH_TOKEN_KEY, value="", expired=True)
    )


@router.get(
    "/forget-password/{email}", status_code=status.HTTP_200_OK, response_model=None
)
async def forget_password(user: User = Depends(valid_user_email)) -> None:
    send_forget_password_email.delay(
        email_to=user.email,
        token=create_forget_password_token(user=user),
        full_name=user.full_name,
    )


@router.patch(
    "/new-password/{token}", status_code=status.HTTP_200_OK, response_model=None
)
async def create_new_password(user: User = Depends(change_forgotten_password)):
    return user.to_dict()


@router.get(
    "/validate-access-token", status_code=status.HTTP_200_OK, response_model=bool
)
async def validate_access_token(
    valid_access_token: bool = Depends(validate_access_token_dependency),
):
    return valid_access_token


@router.patch("/update-profile", status_code=status.HTTP_200_OK, response_model=None)
async def update_user_profile(user: User = Depends(update_user_profile_dependency)):
    return user.to_dict()


@router.patch("/update-phone", status_code=status.HTTP_200_OK, response_model=None)
async def update_user_phone(user: User = Depends(update_user_phone_dependency)):
    return user.to_dict()


@router.patch(
    "/change-old-password", status_code=status.HTTP_200_OK, response_model=None
)
async def change_old_password(user: User = Depends(change_old_password_dependency)):
    return user.to_dict()


@router.delete(
    "/delete-my-account", status_code=status.HTTP_200_OK, response_model=None
)
async def delete_my_account(result: None = Depends(delete_my_account_dependency)):
    return result
