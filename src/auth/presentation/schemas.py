from typing import Any, Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    constr,
    field_validator,
    model_validator,
)

from src.auth.validators import validate_phone_number


class LoginUserScheme(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

    @model_validator(mode="before")
    @classmethod
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        if isinstance(data, dict):
            return {**data}

        elif isinstance(data, bytes):
            from urllib.parse import unquote

            query_params = unquote(data).split("=")
            email = query_params[2].split("&")[0]
            password = query_params[3]
            return {"email": email, "password": password}

        else:
            return {**data.__dict__}

    @field_validator("email", mode="before")
    @classmethod
    def email_to_lower(cls, value: str) -> str:
        return value.lower()


class UpdateUserProfileScheme(BaseModel):
    middle_name: Optional[constr(min_length=2, max_length=50)] = None
    last_name: Optional[constr(min_length=2, max_length=50)] = None


class RegisterUserScheme(LoginUserScheme, UpdateUserProfileScheme):
    first_name: constr(min_length=2, max_length=50)
    phone: str

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone_with_regex(cls, value: str) -> str:
        return validate_phone_number(phone=value)


class UpdateUserPhoneScheme(BaseModel):
    phone: str
    is_phone_number_confirmed: bool = True

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone_with_regex(cls, value: str) -> str:
        return validate_phone_number(phone=value)


class ChangeForgottenPasswordScheme(BaseModel):
    new_password: str = Field(min_length=8, max_length=64)


class ChangeOldPasswordScheme(ChangeForgottenPasswordScheme):
    old_password: str = Field(min_length=8, max_length=64)
