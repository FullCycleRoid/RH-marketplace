from pprint import pprint
from time import time
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from utils.pipelines.connector import MarketplaceDBSession
from src import Company, CompanyField, CompanyFieldType, CompanyOKVED, Manager, FieldTypeTranslation


def get_company_by_id_marketplace(
        company_id: str,
        lang: str = 'RU',
        _session: Session = MarketplaceDBSession
) -> Optional[dict]:
    """Получение полной информации о компании с переводами и связанными данными"""
    with _session() as session:
        company = (
            session.query(Company)
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
            .filter(Company.id == company_id)
            .first()
        )

        if not company:
            return None

        return {
            "id": str(company.id),
            "country_code": company.country_code,
            "legal_status": company.legal_status.name,
            "system_status": company.system_status.name,
            "created_at": company.created_at.isoformat(),
            "updated_at": company.updated_at.isoformat(),
            "translations": [
                {"lang": t.language_code, "name": t.name}
                for t in company.translations
            ],
            "fields": [
                {
                    "code": field.code,
                    "value": next(
                        (ft.data for ft in field.translations
                         if ft.language_code == lang),
                        field.code
                    ),
                    "name": next(
                        (ftt.name for ftt in field.field_type.translations
                         if ftt.language_code == lang),
                        str(field.company_field_type_id)
                    ),
                    "data_type": field.field_type.data_type.name
                }
                for field in company.fields
            ],
            "managers": [
                {
                    "position": manager.position.name,
                    "inn": manager.inn,
                    "since_on_position": manager.since_on_position.isoformat() if manager.since_on_position else None,
                    "name": next(
                        (mt.full_name for mt in manager.translations
                         if mt.language_code == lang),
                        "No name"
                    )
                }
                for manager in company.managers
            ],
            "okveds": [
                {
                    "code": okved.okved.code,
                    "name": okved.okved.name,
                }
                for okved in company.okveds
            ],
            "financial_reports": [
                {
                    "year": report.year,
                    "annual_income": float(report.annual_income) if report.annual_income else None,
                    "net_profit": float(report.net_profit) if report.net_profit else None,
                    "currency": report.currency
                }
                for report in company.financial_reports
            ],
            "tax_reports": [
                {
                    "year": report.year,
                    "taxes_paid": report.taxes_paid,
                    "paid_insurance": report.paid_insurance
                }
                for report in company.tax_reports
            ],
            "contacts": [
                {
                    "type": contact.type.name,
                    "data": contact.data,
                    "is_verified": contact.is_verified
                }
                for contact in company.contacts
            ]
        }

from sqlalchemy import and_, or_

def get_companies_by_inn(inn_value: str, lang: str = 'RU', session: Session = MarketplaceDBSession) -> List[dict]:
    """Поиск компаний по INN через код поля с исправленной фильтрацией"""
    with session() as db_session:
        # Основной запрос с явными джойнами
        query = (
            db_session.query(Company)
            .join(Company.fields)
            .join(CompanyField.field_type)
            .join(
                FieldTypeTranslation,
                and_(
                    FieldTypeTranslation.field_type_id == CompanyFieldType.id,
                    FieldTypeTranslation.language_code == lang
                )
            )
            .filter(
                CompanyField.code == inn_value,
                or_(
                    FieldTypeTranslation.name.ilike('инн'),
                    FieldTypeTranslation.name.ilike('inn')
                )
            )
            .options(
                joinedload(Company.translations),
                joinedload(Company.fields)
                .joinedload(CompanyField.translations),
                joinedload(Company.fields)
                .joinedload(CompanyField.field_type)
                .joinedload(CompanyFieldType.translations),  # Исправлено здесь
                joinedload(Company.managers)
                .joinedload(Manager.translations),
                joinedload(Company.okveds)
                .joinedload(CompanyOKVED.okved),
                )
        )

        companies = query.all()

        result = []
        for company in companies:
            # Получаем дату регистрации
            registration_date = next(
                (f.datetime_data.isoformat() if f.datetime_data else None
                 for f in company.fields
                 if any(
                    t.name.lower() == 'дата_регистрации'
                    for t in f.field_type.translations
                )),
                None
            )

            result.append({
                "id": str(company.id),
                "name": next(
                    (t.name for t in company.translations
                     if t.language_code == lang),
                    "No name"
                ),
                "inn": inn_value,
                "okveds": [okved.okved.code for okved in company.okveds],
                "registration_date": registration_date,
                "managers": [
                    {
                        "name": next(
                            (mt.full_name for mt in m.translations
                             if mt.language_code == lang),
                            "No name"
                        ),
                        "position": m.position.name
                    }
                    for m in company.managers
                ]
            })

        return result

start = time()
# company = get_company_by_id_marketplace(company_id='00022e80-ccf9-4b47-9b29-a4fa45aaf987')
company = get_companies_by_inn(inn_value='7804576823')
pprint(company)
elapsed = time() - start
print('Time', elapsed)