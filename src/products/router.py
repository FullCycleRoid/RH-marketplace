from fastapi import APIRouter, Depends, status

from src.auth.dependencies import get_my_account as get_my_account_dependency
from src.auth.models import User


router = APIRouter()


@router.post("/send", status_code=status.HTTP_200_OK, response_model=None)
async def send_new_message(user: User = Depends(get_my_account_dependency)):
    message = {}
    return message


@router.get("/chat_history", status_code=status.HTTP_200_OK, response_model=None)
async def chat_history(user: User = Depends(get_my_account_dependency)):
    history = {}
    return history


@router.get("/all_chats", status_code=status.HTTP_200_OK, response_model=None)
async def all_chats(user: User = Depends(get_my_account_dependency)):
    chats = {}
    return chats
