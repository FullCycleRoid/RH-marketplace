from fastapi import Depends, status

from src.company.router import router
from src.user.infrastructure.models import User
from src.user.presentation.dependencies import (
    get_my_account as get_my_account_dependency,
)


@router.put("/edit_about", status_code=status.HTTP_200_OK, response_model=None)
async def edit_about_company_section(user: User = Depends(get_my_account_dependency)):
    # проверить что пользователь состоит в этой компании и имеет права для редактирования раздела О компании
    company = {}
    return company
