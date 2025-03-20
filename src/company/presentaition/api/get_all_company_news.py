from fastapi import Depends, status

from src.company.router import router
from src.user.infrastructure.models import User
from src.user.presentation.dependencies import \
    get_my_account as get_my_account_dependency


@router.get(
    "/all_news/{company_id}", status_code=status.HTTP_200_OK, response_model=None
)
async def get_all_news(user: User = Depends(get_my_account_dependency)):
    company = {}
    return company
