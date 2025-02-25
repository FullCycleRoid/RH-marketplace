from pydantic import BaseModel
from typing import List, Optional


# Схема для создания менеджера
class ManagerCreate(BaseModel):
    username: str
    company_id: int

# Схема для ответа с деталями менеджера
class ManagerResponse(ManagerCreate):
    id: int

    class Config:
        orm_mode = True

# Схема для создания диалога
class DialogueCreate(BaseModel):
    company_a_id: int
    company_b_id: int

# Схема для ответа с деталями диалога
class DialogueResponse(DialogueCreate):
    id: int
    messages: List["MessageResponse"] = []  # Вложенные сообщения диалога

    class Config:
        orm_mode = True

# Схема для создания сообщения
class MessageCreate(BaseModel):
    content: str
    manager_id: int
    dialogue_id: int

# Схема для ответа с деталями сообщения
class MessageResponse(MessageCreate):
    id: int
    timestamp: str  # Время отправки сообщения

    class Config:
        orm_mode = True