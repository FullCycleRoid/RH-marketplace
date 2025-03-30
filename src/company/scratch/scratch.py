from pprint import pprint
from time import time
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload

from utils.pipelines.connector import MarketplaceDBSession
from src import Company, CompanyField, CompanyFieldType, Manager, CompanyOKVED, FieldTranslation


class CompanySerializer:
    """Класс для преобразования объекта Company в словарь"""

    def __init__(self, company: 'Company', lang: str = 'RU'):
        self.company = company
        self.lang = lang

    def to_dict(self) -> Dict[str, Any]:
        """Основной метод сериализации"""
        return {
            **self._basic_info(),
            **self._translations(),
            **self._fields_info(),
            **self._managers_info(),
            **self._okveds_info(),
            **self._financial_info(),
            **self._tax_info(),
            **self._contacts_info(),
            **self._system_info()
        }

    def _basic_info(self) -> Dict[str, Any]:
        """Базовая информация о компании"""
        return {
            "id": str(self.company.id),
            "country_code": self.company.country_code,
            "legal_status": self.company.legal_status.name,
            "system_status": self.company.system_status.name,
            "created_at": self.company.created_at.isoformat(),
            "updated_at": self.company.updated_at.isoformat()
        }

    def _translations(self) -> Dict[str, Any]:
        """Обработка переводов названия компании"""
        return {
            "translations": [
                {"lang": t.language_code, "name": t.name}
                for t in self.company.translations
            ]
        }

    def _fields_info(self) -> Dict[str, Any]:
        """Обработка полей компании"""
        return {
            "fields": [
                self._serialize_field(field)
                for field in self.company.fields
            ]
        }

    def _serialize_field(self, field: 'CompanyField') -> Dict[str, Any]:
        """Сериализация одного поля"""
        return {
            "code": field.code,
            "value": self._get_field_value(field),
            "name": self._get_field_type_name(field),
            "data_type": field.field_type.data_type.name
        }

    def _get_field_value(self, field: 'CompanyField') -> Optional[str]:
        """Получение значения поля с учетом переводов"""
        translation = next(
            (ft.data for ft in field.translations
             if ft.language_code == self.lang),
            None
        )
        return translation or field.code

    def _get_field_type_name(self, field: 'CompanyField') -> str:
        """Получение названия типа поля"""
        return next(
            (ftt.name for ftt in field.field_type.translations
             if ftt.language_code == self.lang),
            str(field.company_field_type_id)
        )

    def _managers_info(self) -> Dict[str, Any]:
        """Обработка информации о менеджерах"""
        return {
            "managers": [
                {
                    "inn": manager.inn,
                    "name": self._get_manager_name(manager),
                    "position": manager.position.name,
                    "since_on_position": manager.since_on_position.isoformat()
                    if manager.since_on_position else None
                }
                for manager in self.company.managers
            ]
        }

    def _get_manager_name(self, manager: 'Manager') -> str:
        """Получение имени менеджера с учетом переводов"""
        return next(
            (mt.full_name for mt in manager.translations
             if mt.language_code == self.lang),
            "No name"
        )

    def _okveds_info(self) -> Dict[str, Any]:
        """Обработка кодов ОКВЭД"""
        return {
            "okveds": [
                {
                    "code": okved.okved.code,
                    "name": okved.okved.name
                }
                for okved in self.company.okveds
            ]
        }

    def _financial_info(self) -> Dict[str, Any]:
        """Финансовые отчеты"""
        return {
            "financial_reports": [
                {
                    "year": report.year,
                    "annual_income": float(report.annual_income)
                    if report.annual_income else None,
                    "net_profit": float(report.net_profit)
                    if report.net_profit else None,
                    "currency": report.currency
                }
                for report in self.company.financial_reports
            ]
        }

    def _tax_info(self) -> Dict[str, Any]:
        """Налоговые отчеты"""
        return {
            "tax_reports": [
                {
                    "year": report.year,
                    "taxes_paid": report.taxes_paid,
                    "paid_insurance": report.paid_insurance
                }
                for report in self.company.tax_reports
            ]
        }

    def _contacts_info(self) -> Dict[str, Any]:
        """Контактная информация"""
        return {
            "contacts": [
                {
                    "type": contact.type.name,
                    "data": contact.data,
                    "is_verified": contact.is_verified
                }
                for contact in self.company.contacts
            ]
        }

    def _system_info(self) -> Dict[str, Any]:
        """Системная информация"""
        return {
            "system_status": self.company.system_status.name,
            "legal_status": self.company.legal_status.name
        }

class CompanyQueryManager:
    """Класс для управления запросами к компаниям"""

    def __init__(self, session: Session):
        self.session = session

    def base_query(self):
        """Базовый запрос с корректными JOIN'ами"""
        return (
            self.session.query(Company)
            .options(
                joinedload(Company.translations),
                joinedload(Company.fields)
                .joinedload(CompanyField.translations),
                joinedload(Company.fields)
                .joinedload(CompanyField.field_type)
                .joinedload(CompanyFieldType.translations),
                joinedload(Company.managers)
                .joinedload(Manager.translations),
                joinedload(Company.contacts),
                joinedload(Company.financial_reports),
                joinedload(Company.tax_reports),
                joinedload(Company.change_logs),
                joinedload(Company.okveds)
                .joinedload(CompanyOKVED.okved),
            )
        )

    def get_by_id(self, company_id: str, lang: str = 'RU') -> Optional[Dict]:
        """Получение компании по ID"""
        company = (
            self.base_query()
            .filter(Company.id == company_id)
            .first()
        )
        return CompanySerializer(company, lang).to_dict() if company else None

    def get_by_inn(self, inn_value: str, lang: str = 'RU') -> List[Dict]:
        """Поиск компаний по ИНН"""
        companies = (
            self.base_query()
            .join(CompanyField.translations)
            .filter(
                FieldTranslation.data == inn_value,
                CompanyField.code.in_(["INN", "inn", "инн", "иин"])
            )
            .all()
        )
        return [CompanySerializer(c, lang).to_dict() for c in companies]

# Пример использования
with MarketplaceDBSession() as session:
    manager = CompanyQueryManager(session)

    start = time()
    # Получение компании по ID
    # company = manager.get_by_id('00022e80-ccf9-4b47-9b29-a4fa45aaf987')
    # pprint(company)


    # Поиск по ИНН
    companies = manager.get_by_inn('7804576823')

    pprint(companies)
    elapsed = time() - start
    print('Time', elapsed)