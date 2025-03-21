import re
from datetime import datetime
from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from pipelines.connector import ClusterDBSession, MarketplaceDBSession
from pipelines.raw_model import RawCompany
from src import CompanyFieldType, OkvedNode
from src.core.logger import logger


def get_active_companies(offset: int, BATCH_SIZE: int,  _session: Session = ClusterDBSession):
    with _session() as session:
        res = session.query(RawCompany).filter(RawCompany.legal_name != "Индивидуальный предприниматель").limit(BATCH_SIZE).offset(offset).all()
        return res


def get_company_okved(offset: int, BATCH_SIZE: int,  _session: Session = ClusterDBSession):
    with _session() as session:
        res = session.query(RawCompany.okved).limit(BATCH_SIZE).offset(offset).all()
        return res


def get_random_company_okved(BATCH_SIZE: int = 10000, _session: Session = ClusterDBSession):
    with _session() as session:
        # Случайным образом упорядочиваем записи и выбираем BATCH_SIZE записей
        res = session.query(RawCompany.okved).order_by(func.random()).limit(BATCH_SIZE).all()
        return res


def get_total_count(_session: Session = ClusterDBSession):
    with _session() as session:
        return session.query(func.count(RawCompany.id)).scalar()


def get_active_company_count(_session: Session = ClusterDBSession):
    with _session() as session:
        count = session.query(func.count()).filter(
            or_(
                RawCompany.legal_entity_state == "Действующая компания",
                RawCompany.legal_entity_state == "Действующая организация",
                RawCompany.legal_entity_state.startswith("Юридическое лицо ликвидировано")
            )
        ).scalar()
        return count


def get_entrepreneurs(offset: int, BATCH_SIZE: int,  _session: Session = ClusterDBSession):
    with _session() as session:
        res = session.query(RawCompany).filter(RawCompany.legal_entity_state == "Действующее ИП").limit(BATCH_SIZE).offset(offset).all()
        return res


MONTHS = {
    'января': 'January',
    'февраля': 'February',
    'марта': 'March',
    'апреля': 'April',
    'мая': 'May',
    'июня': 'June',
    'июля': 'July',
    'августа': 'August',
    'сентября': 'September',
    'октября': 'October',
    'ноября': 'November',
    'декабря': 'December'
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
            "трлн": 1_000_000_000_000
        }

        return int(number * multipliers.get(unit, 1))
    except:
        return 0


def get_okved_by_code(code: str, _session: Session = MarketplaceDBSession) -> Optional[str]:
    with _session() as session:
        res = session.query(OkvedNode).filter(OkvedNode.code == code).first()
        if res is None:
            print("Код не найден в базе данных")
        return res


def get_all_field_types(_session: Session = MarketplaceDBSession) -> Optional[CompanyFieldType]:
    with _session() as session:
        res = session.query(CompanyFieldType).all()
        if res is None:
            print("Типы полей не найдены в базе данных")
        return res