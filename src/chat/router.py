from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.chat import models, schemas
from src.core.database.postgres.connectors import get_db

router = APIRouter()


@router.post("/dialogues/", response_model=schemas.DialogueResponse)
def create_dialogue(dialogue: schemas.DialogueCreate, db: Session = Depends(get_db)):
    # Проверка существования компаний
    company_a = db.query(models.Company).filter(models.Company.id == dialogue.company_a_id).first()
    company_b = db.query(models.Company).filter(models.Company.id == dialogue.company_b_id).first()
    if not company_a or not company_b:
        raise HTTPException(status_code=404, detail="One or both companies not found")

    # Создание нового диалога
    db_dialogue = models.Dialogue(
        company_a_id=dialogue.company_a_id,
        company_b_id=dialogue.company_b_id
    )
    db.add(db_dialogue)
    db.commit()
    db.refresh(db_dialogue)
    return db_dialogue


@router.get("/dialogues/company/{company_id}", response_model=List[schemas.DialogueResponse])
def get_dialogues_by_company(company_id: int, db: Session = Depends(get_db)):
    dialogues = (
        db.query(models.Dialogue)
        .filter(
            (models.Dialogue.company_a_id == company_id) | (models.Dialogue.company_b_id == company_id)
        )
        .all()
    )
    if not dialogues:
        raise HTTPException(status_code=404, detail="Dialogues not found")
    return dialogues


@router.get("/dialogues/between/{company_a_id}/{company_b_id}", response_model=List[schemas.DialogueResponse])
def get_dialogues_between_companies(company_a_id: int, company_b_id: int, db: Session = Depends(get_db)):
    dialogues = (
        db.query(models.Dialogue)
        .filter(
            (models.Dialogue.company_a_id == company_a_id) & (models.Dialogue.company_b_id == company_b_id) |
            (models.Dialogue.company_a_id == company_b_id) & (models.Dialogue.company_b_id == company_a_id)
        )
        .all()
    )
    if not dialogues:
        raise HTTPException(status_code=404, detail="Dialogues not found")
    return dialogues


@router.post("/messages/", response_model=schemas.MessageResponse)
def send_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    # Проверка существования диалога и менеджера
    dialogue = db.query(models.Dialogue).filter(models.Dialogue.id == message.dialogue_id).first()
    manager = db.query(models.Manager).filter(models.Manager.id == message.manager_id).first()
    if not dialogue or not manager:
        raise HTTPException(status_code=404, detail="Dialogue or manager not found")

    # Создание нового сообщения
    db_message = models.Message(
        content=message.content,
        timestamp=datetime.utcnow(),
        manager_id=message.manager_id,
        dialogue_id=message.dialogue_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


@router.get("/messages/{dialogue_id}", response_model=List[schemas.MessageResponse])
def get_messages_by_dialogue(dialogue_id: int, db: Session = Depends(get_db)):
    messages = db.query(models.Message).filter(models.Message.dialogue_id == dialogue_id).all()
    if not messages:
        raise HTTPException(status_code=404, detail="Messages not found")
    return messages