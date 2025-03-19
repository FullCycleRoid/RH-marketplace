from fastapi import Depends, status

from src.company.router import router
from src.user.presentation.dependencies import get_my_account as get_my_account_dependency
from src.user.infrastructure.models import User


@router.post(
    "/company_loader", status_code=status.HTTP_201_CREATED, response_model=None
)
async def create_company(user: User = Depends(get_my_account_dependency)):
    # проверить что у пользователя нет уже созданных компаний
    # проверить что компания не существует уже в базе компаний РФ
    company = {}
    return company
