from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy import select

from src.core.database.connectors import fetch_one, fetch_all
from src.marketplace.user.models import User

router = APIRouter()


@router.get("/test", status_code=status.HTTP_200_OK, response_model=Optional[User])
async def test_route():
    stmt = select(User)
    res = await fetch_all(stmt)
    print(res)
