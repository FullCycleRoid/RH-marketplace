from typing import Optional
from pydantic import BaseModel


class UpdateUserSchema(BaseModel):
    id: int

    role_id: Optional[int] = None

    telegram_username: Optional[str] = None
    telegram_id: Optional[str] = None

    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None

    email: Optional[str] = None
    phone: Optional[str] = None

    is_email_confirm: Optional[bool] = None
    is_phone_number_confirm: Optional[bool] = None
    