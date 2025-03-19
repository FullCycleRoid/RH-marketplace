from fastapi import Depends, status

from src.company.router import router
from src.user.dependencies import get_my_account as get_my_account_dependency
from src.user.models import User


@router.put(
    "/edit_news/{company_id}", status_code=status.HTTP_200_OK, response_model=None
)
async def delete_news(user: User = Depends(get_my_account_dependency)):
    # проверить что пользователь состоит в этой компании и имеет права для удаления новостей
    company = {}
    return company
