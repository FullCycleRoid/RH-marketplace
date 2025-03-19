from fastapi import Depends, status

from src.company.router import router
from src.user.dependencies import get_my_account as get_my_account_dependency
from src.user.models import User


@router.get("/inactivate_company", status_code=status.HTTP_200_OK, response_model=None)
async def inactivate_company(user: User = Depends(get_my_account_dependency)):
    # проверить что пользователь состоит в этой компании и имеет права для деактивации компании
    company = {}
    return company
