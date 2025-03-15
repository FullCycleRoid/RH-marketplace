from fastapi import APIRouter, Depends, status

from src.auth.dependencies import get_my_account as get_my_account_dependency

from src.auth.models import User
from src.auth.security import create_verify_email_token
from src.tasks.tasks import send_verify_email_message


router = APIRouter()


@router.post("/company_loader", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_company(user: User = Depends(get_my_account_dependency)):
    # проверить что у пользователя нет уже созданных компаний
    # проверить что компания не существует уже в базе компаний РФ
    company = {}
    return company


@router.put("/edit_about", status_code=status.HTTP_200_OK, response_model=None)
async def edit_company_about_section(user: User = Depends(get_my_account_dependency)):
    # проверить что пользователь состоит в этой компании и имеет права для редактирования раздела О компании
    company = {}
    return company


@router.get("/inactivate_company", status_code=status.HTTP_200_OK, response_model=None)
async def inactivate_company(user: User = Depends(get_my_account_dependency)):
    # проверить что пользователь состоит в этой компании и имеет права для деактивации компании
    company = {}
    return company


@router.get("/all_news/{company_id}", status_code=status.HTTP_200_OK, response_model=None)
async def get_all_news(user: User = Depends(get_my_account_dependency)):
    company = {}
    return company


@router.post("/create_news/{company_id}", status_code=status.HTTP_200_OK, response_model=None)
async def create_news(user: User = Depends(get_my_account_dependency)):
    # проверить что пользователь состоит в этой компании и имеет права для создания новостей
    company = {}
    return company


@router.put("/edit_news/{company_id}", status_code=status.HTTP_200_OK, response_model=None)
async def edit_news(user: User = Depends(get_my_account_dependency)):
    # проверить что пользователь состоит в этой компании и имеет права для редактирования новостей
    company = {}
    return company


@router.put("/edit_news/{company_id}", status_code=status.HTTP_200_OK, response_model=None)
async def delete_news(user: User = Depends(get_my_account_dependency)):
    # проверить что пользователь состоит в этой компании и имеет права для удаления новостей
    company = {}
    return company

