import random
import re
from datetime import datetime
from typing import List, Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from utils.pipelines.connector import ClusterDBSession, MarketplaceDBSession
from utils.pipelines.raw_model import RawCompany
from src import Company, CompanyField, CompanyFieldType, OkvedNode, FieldTypeTranslation, FieldTranslation
from src.core.logger import logger


def get_active_companies(
    offset: int, BATCH_SIZE: int, _session: Session = ClusterDBSession
):
    with _session() as session:
        res = (
            session.query(RawCompany)
            .filter(RawCompany.legal_name != "Индивидуальный предприниматель")
            .filter(RawCompany.legal_name.isnot(None))  # или .filter(RawCompany.legal_name != None)
            .limit(BATCH_SIZE)
            .offset(offset)
            .all()
        )
        return res


def get_company_okved(
    offset: int, BATCH_SIZE: int, _session: Session = ClusterDBSession
):
    with _session() as session:
        res = session.query(RawCompany.okved).limit(BATCH_SIZE).offset(offset).all()
        return res


def get_random_company_okved(
    BATCH_SIZE: int = 10000, _session: Session = ClusterDBSession
):
    with _session() as session:
        # Случайным образом упорядочиваем записи и выбираем BATCH_SIZE записей
        res = (
            session.query(RawCompany.okved)
            .order_by(func.random())
            .limit(BATCH_SIZE)
            .all()
        )
        return res


def get_total_count(_session: Session = ClusterDBSession):
    with _session() as session:
        return session.query(func.count(RawCompany.id)).scalar()


def get_active_company_count(_session: Session = ClusterDBSession):
    with _session() as session:
        count = (
            session.query(func.count())
            .filter(
                or_(
                    RawCompany.legal_entity_state == "Действующая компания",
                    RawCompany.legal_entity_state == "Действующая организация",
                    RawCompany.legal_entity_state.startswith(
                        "Юридическое лицо ликвидировано"
                    ),
                )
            )
            .scalar()
        )
        return count


def get_entrepreneurs(
    offset: int, BATCH_SIZE: int, _session: Session = ClusterDBSession
):
    with _session() as session:
        res = (
            session.query(RawCompany)
            .filter(RawCompany.legal_entity_state == "Действующее ИП")
            .limit(BATCH_SIZE)
            .offset(offset)
            .all()
        )
        return res


MONTHS = {
    "января": "January",
    "февраля": "February",
    "марта": "March",
    "апреля": "April",
    "мая": "May",
    "июня": "June",
    "июля": "July",
    "августа": "August",
    "сентября": "September",
    "октября": "October",
    "ноября": "November",
    "декабря": "December",
}


def convert_ru_date_to_date_obj(raw_date: str) -> Optional[datetime]:
    month_replaced = False
    for ru_month, en_month in MONTHS.items():
        if ru_month in raw_date:
            date_str = raw_date.replace(ru_month, en_month)
            month_replaced = True
            break

    if not month_replaced:
        logger.info(f"Month not found in registration date: {raw_date}")
        return

    try:
        date_obj = datetime.strptime(date_str, "%d %B %Y года")
        return date_obj.date()

    except ValueError as err:
        logger.info(f"Registration date convert error: {err}")


def convert_to_numeric(value):
    try:
        # Извлекаем числовую часть и единицы измерения
        match = re.search(r"(-?\d[\d\.,]*)\s*(тыс|млн|млрд|трлн)?\.?\s*руб", value)
        if not match:
            return 0

        number = float(match.group(1).replace(",", ".").replace(" ", ""))
        unit = match.group(2)

        multipliers = {
            "тыс": 1_000,
            "млн": 1_000_000,
            "млрд": 1_000_000_000,
            "трлн": 1_000_000_000_000,
        }

        return int(number * multipliers.get(unit, 1))
    except:
        return 0


def get_okved_by_code(
    code: str, _session: Session = MarketplaceDBSession
) -> Optional[str]:
    with _session() as session:
        res = session.query(OkvedNode).filter(OkvedNode.code == code).first()
        if res is None:
            print("Код не найден в базе данных")
        return res


def get_all_field_types(
    _session: Session = MarketplaceDBSession,
) -> List[CompanyFieldType]:
    with _session() as session:
        return session.query(CompanyFieldType).options(joinedload(CompanyFieldType.translations)).all()


def get_random_proxy_obj(proxies: List[str]):
    return {"https": random.choice(proxies)}


def get_company_by_inn(session, inn: str):
    """
    Retrieve a Company by its 'inn' field from the CompanyField table.

    :param session: SQLAlchemy session
    :param inn: The INN value to search for
    :return: The Company object if found, otherwise None
    """
    from sqlalchemy.orm import joinedload
    from sqlalchemy import or_, and_

    company = (
        session.query(Company)
        .join(CompanyField, Company.id == CompanyField.company_id)
        .join(CompanyFieldType, CompanyField.company_field_type_id == CompanyFieldType.id)
        .join(
            FieldTypeTranslation,
            and_(
                CompanyFieldType.id == FieldTypeTranslation.field_type_id,
                FieldTypeTranslation.language_code == "EN",
                FieldTypeTranslation.name == "inn"
            )
        )
        .outerjoin(
            FieldTranslation,
            and_(
                CompanyField.id == FieldTranslation.field_id,
                FieldTranslation.language_code == "RU"
            )
        )
        .filter(
            or_(
                FieldTranslation.data == inn
            )
        )
        .options(joinedload(Company.fields))
        .first()
    )
    return company
