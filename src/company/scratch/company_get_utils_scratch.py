import random
import re
from datetime import datetime
from pprint import pprint
from typing import List, Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload, contains_eager

from pipelines.connector import ClusterDBSession, MarketplaceDBSession
from pipelines.raw_model import RawCompany
from src import Company, CompanyField, CompanyFieldType, OkvedNode, FieldTypeTranslation, FieldTranslation, \
    CompanyOKVED, Manager
from src.core.logger import logger


def get_company_by_id_marketplace(company_id: str, lang: str = 'RU', _session: Session = MarketplaceDBSession):
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
                )
            .filter(Company.id == company_id)
            .first()
        )

        if not company:
            return None

        return {
            "id": str(company.id),
            "country_code": company.country_code,
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
                        field.code  # fallback to code if no translation
                    ),
                    "name": next(
                        (ftt.name for ftt in field.field_type.translations
                         if ftt.language_code == lang),
                        field.company_field_type_id  # fallback to type ID
                    )
                }
                for field in company.fields
            ],
            "managers": [
                {
                    "inn": manager.inn,
                    "name": next(
                        (mt.full_name for mt in manager.translations
                         if mt.language_code == lang),
                        "No name"
                    )
                }
                for manager in company.managers
            ]
        }

def get_companies_by_inn(session, inn_value):
    companies = (
        session.query(Company)
        .join(Company.fields)
        .join(CompanyField.translations)
        .filter(
            FieldTranslation.data == inn_value,
            CompanyField.code.in_(["INN", "inn", "инн", "иин"])
        )
        .options(
            contains_eager(Company.fields)
            .contains_eager(CompanyField.translations),
            # Повторить для остальных связей как в первом запросе
        )
        .all()
    )
    return companies
#
#
# def company_to_dict(company):
#     return {
#         "id": str(company.id),
#         "country_code": company.country_code,
#         "translations": [{
#             "lang": t.language_code,
#             "name": t.name
#         } for t in company.translations],
#         "fields": [{
#             "code": field.code,
#             "translations": [{
#                 "lang": ft.language_code,
#                 "data": ft.data
#             } for ft in field.translations]
#         } for field in company.fields],
#         "managers": [{
#             "inn": m.inn,
#             "translations": [{
#                 "lang": mt.language_code,
#                 "name": mt.full_name
#             } for mt in m.translations]
#         } for m in company.managers],
#         # Добавьте остальные поля аналогичным образом
#     }

company = get_company_by_id_marketplace(company_id='00022e80-ccf9-4b47-9b29-a4fa45aaf987')
# get_companies_by_inn
# company = get_companies_by_inn(inn_value='')
pprint(company)