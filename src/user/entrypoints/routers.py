from typing import Optional

from fastapi import APIRouter, status
from sqlalchemy import select

from src.user.domain.models import User
from src.user.schemas import UpdateUserSchema

router = APIRouter()


@router.get("/me", status_code=status.HTTP_200_OK, response_model=Optional[User])
async def get_me():
    stmt = select(User)
    # res = await fetch_all(stmt)
    # print(res)


@router.put("/me", status_code=status.HTTP_200_OK, response_model=Optional[User])
async def update_user(update_user: UpdateUserSchema):
    print('Update user schema data', update_user)


@router.post("/registration", status_code=status.HTTP_200_OK, response_model=Optional[User])
async def registration_user(update_user: UpdateUserSchema):
    print('Update user schema data', update_user)

