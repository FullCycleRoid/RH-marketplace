import uuid
from datetime import datetime
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pipelines.company_loader.context import CompanyDTO
from pipelines.generic_pipeline import Context, NextStep, PipelineStep
from pipelines.utils import get_company_by_inn
from src import (Company, CompanyOKVED, Contact, FinancialReport, Manager,
                 TaxReport, CompanyFieldType, FieldTypeTranslation, CompanyTranslation, FieldTranslation, CompanyField)
from src.company.enums import TranslationMode


class BuildCompanyDBModel(PipelineStep):
    _sessionmaker = None

    def __init__(self):
        self.field_type_cache = {}  # Кэш для типов полей { (country_code, name): id }

    def _cache_field_types(self, session):
        """Загружаем типы полей и их переводы в кэш"""
        field_types = session.query(CompanyFieldType).all()
        translations = session.query(FieldTypeTranslation).filter_by(language_code='ru').all()

        for ft in field_types:
            translation = next((t for t in translations if t.field_type_id == ft.id), None)
            if translation:
                key = (ft.country_code, translation.name)
                self.field_type_cache[key] = ft.id

    def _get_field_type_id(self, country_code: str, field_name_ru: str) -> uuid.UUID:
        """Получаем ID типа поля по русскому названию"""
        return self.field_type_cache.get((country_code, field_name_ru))

    def __call__(self, context: Context, next_step: NextStep) -> None:
        if BuildCompanyDBModel._sessionmaker is None:
            async_postgres_uri = (
                "postgresql+psycopg2://admin:password123@localhost:25432/monolith"
            )
            psycopg_engine = create_engine(
                async_postgres_uri, echo=False, pool_size=200
            )
            BuildCompanyDBModel._sessionmaker = sessionmaker(
                bind=psycopg_engine,
                autoflush=False,
                expire_on_commit=False,
                autocommit=False,
            )

        with BuildCompanyDBModel._sessionmaker() as session:
            self._cache_field_types(session)
        ctx_company = context.company_dto

        if not get_company_by_inn(session, ctx_company.inn):
            company = Company(
                country_code=ctx_company.country_code,
                legal_status=ctx_company.legal_status,
                system_status=ctx_company.system_status,
            )
            session.add(company)
            session.flush()

            # Добавление основных полей компании
            fields_mapping = [
                ('name', 'Название компании', ctx_company.name),
                ('legal_name', 'Юридическое название', ctx_company.legal_name),
                ('inn', 'ИНН', ctx_company.inn),
                ('ogrn', 'ОГРН', ctx_company.ogrn),
                ('okpo', 'ОКПО', ctx_company.okpo),
                ('registration_date', 'Дата регистрации', ctx_company.registration_date),
                ('okato_code', 'ОКАТО', ctx_company.okato_code),
                ('oktmo_code', 'ОКТМО', ctx_company.oktmo_code),
                ('okogu_code', 'ОКОГУ', ctx_company.okogu_code),
                ('okopf_code', 'ОКОПФ', ctx_company.okopf_code),
                ('okfs_code', 'ОКФС', ctx_company.okfs_code),
            ]

            for field_name, ru_name, value in fields_mapping:
                if value is None:
                    continue

                field_type_id = self._get_field_type_id(ctx_company.country_code, ru_name)
                if not field_type_id:
                    continue

                field = CompanyField(
                    company_id=company.id,
                    company_field_type_id=field_type_id,
                    is_translatable=field_name in ['name', 'legal_name'],
                    translation_mode=TranslationMode.AUTO if field_name in ['name', 'legal_name'] else None
                )

                if isinstance(value, datetime.date):
                    field.datetime_data = value
                else:
                    field.ru_data = str(value)

                session.add(field)
                session.flush()

                # Добавляем русский перевод для поля
                if field.is_translatable:
                    translation = FieldTranslation(
                        field_id=field.id,
                        language_code='ru',
                        data=str(value)
                    )
                    session.add(translation)

            # Добавление преимуществ
            if ctx_company.advantages:
                ru_advantages = '\n'.join(ctx_company.advantages)
                company_translation = CompanyTranslation(
                    company_id=company.id,
                    language_code='ru',
                    advantages=ru_advantages
                )
                session.add(company_translation)

            # Финансовые отчеты
            for report in ctx_company.financial_reports:
                financial_report = FinancialReport(
                    company_id=company.id,
                    year=report.year,
                    annual_income=report.annual_income,
                    net_profit=report.net_profit,
                    currency=report.currency
                )
                session.add(financial_report)

            # Налоговые отчеты
            for report in ctx_company.tax_reports:
                tax_report = TaxReport(
                    company_id=company.id,
                    year=report.year,
                    taxes_paid=report.taxes_paid,
                    paid_insurance=report.paid_insurance
                )
                session.add(tax_report)

            # ОКВЭД коды
            for okved_id in ctx_company.okved_ids:
                company_okved = CompanyOKVED(
                    company_id=company.id,
                    okved_id=okved_id
                )
                session.add(company_okved)

            session.commit()

        next_step(context)

