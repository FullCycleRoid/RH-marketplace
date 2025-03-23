import uuid
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pipelines.company_loader.context import CompanyDTO
from pipelines.generic_pipeline import Context, NextStep, PipelineStep
from pipelines.utils import get_company_by_inn
from src import (Company, CompanyOKVED, Contact, FinancialReport, Manager,
                 TaxReport)
from src.company.enums import TranslationMode


class BuildCompanyDBModel(PipelineStep):
    _sessionmaker = None

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
            ctx_company: CompanyDTO = context.company_dto

            company_exists = get_company_by_inn(session, ctx_company.inn)
            if not company_exists:

                field_type_ids: Dict[str, uuid] = context.field_type_ids

                company = Company(
                    country_code=ctx_company.country_code,
                    legal_status=ctx_company.legal_status,
                    system_status=ctx_company.system_status,
                )

                for name, type_id in field_type_ids.items():
                    if name == "name":
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.name,
                            en_data=ctx_company.en_name,
                            is_translatable=True,
                            translation_mode=TranslationMode.AUTO,
                        )
                    if name == "legal_name":
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.legal_name,
                            en_data=ctx_company.en_legal_name,
                            is_translatable=True,
                            translation_mode=TranslationMode.AUTO,
                        )
                    if name == "inn":
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.inn,
                            en_data=ctx_company.inn,
                            is_translatable=False,
                        )
                    if name == "ogrn" and ctx_company.ogrn:
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.ogrn,
                            en_data=ctx_company.ogrn,
                            is_translatable=False,
                        )
                    if name == "kpp" and ctx_company.kpp:
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.kpp,
                            en_data=ctx_company.kpp,
                            is_translatable=False,
                        )
                    if name == "okpo" and ctx_company.okpo:
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.okpo,
                            en_data=ctx_company.okpo,
                            is_translatable=False,
                        )
                    if name == "okogu_code" and ctx_company.okogu_code:
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.okogu_code,
                            en_data=ctx_company.okogu_code,
                            is_translatable=False,
                        )
                    if name == "okopf_code" and ctx_company.okopf_code:
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.okopf_code,
                            en_data=ctx_company.okopf_code,
                            is_translatable=False,
                        )
                    if name == "okfs_code" and ctx_company.okfs_code:
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.okfs_code,
                            en_data=ctx_company.okfs_code,
                            is_translatable=False,
                        )
                    if name == "okato_code" and ctx_company.okato_code:
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.okato_code,
                            en_data=ctx_company.okato_code,
                            is_translatable=False,
                        )
                    if name == "oktmo_code" and ctx_company.oktmo_code:
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.oktmo_code,
                            en_data=ctx_company.oktmo_code,
                            is_translatable=False,
                        )
                    if name == "kladr_code" and ctx_company.code_kladr:
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.code_kladr,
                            en_data=ctx_company.code_kladr,
                            is_translatable=False,
                        )
                    if name == "registration_date" and ctx_company.registration_date:
                        company.add_field(
                            company_field_type_id=type_id,
                            datetime_data=ctx_company.registration_date,
                            is_translatable=False,
                        )
                    if name == "liquidation_date" and ctx_company.liquidation_date:
                        company.add_field(
                            company_field_type_id=type_id,
                            datetime_data=ctx_company.liquidation_date,
                            is_translatable=False,
                        )
                    if name == "authorized_capital" and ctx_company.authorized_capital:
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.authorized_capital,
                            en_data=ctx_company.authorized_capital,
                            is_translatable=False,
                        )
                    if (
                        name == "average_number_of_employees"
                        and ctx_company.average_number_of_employees
                    ):
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ctx_company.average_number_of_employees,
                            en_data=ctx_company.average_number_of_employees,
                            is_translatable=False,
                        )

                    if name == "advantages" and ctx_company.advantages:
                        ru_advantages = ", ".join(ctx_company.advantages)
                        en_advantages = ", ".join(ctx_company.en_advantages)
                        company.add_field(
                            company_field_type_id=type_id,
                            ru_data=ru_advantages,
                            en_data=en_advantages,
                            is_translatable=True,
                            translation_mode=TranslationMode.AUTO,
                        )

                session.add(company)
                session.flush()

                for contact in ctx_company.contacts:
                    contact_obj = Contact(
                        type=contact.type,
                        data=contact.value,
                        is_verified=contact.is_verified,
                    )
                    company.add_contact(contact_obj)

                for manager in ctx_company.management:
                    manager_obj = Manager(
                        position=manager.position,
                        full_name=manager.full_name,
                        en_full_name=manager.en_full_name,
                        inn=manager.inn,
                        since_on_position=manager.since_on_position,
                    )
                    company.add_manager(manager_obj)

                for report in ctx_company.tax_reports:
                    if report.taxes_paid and report.paid_insurance:
                        report_obj = TaxReport(
                            year=report.year,
                            taxes_paid=report.taxes_paid,
                            paid_insurance=report.paid_insurance,
                        )
                        company.add_tax_report(report_obj)

                for report in ctx_company.financial_reports:
                    if report.annual_income or report.net_profit:
                        report_obj = FinancialReport(
                            year=report.year,
                            currency=report.currency,
                            annual_income=report.annual_income,
                            net_profit=report.net_profit,
                        )
                        company.add_financial_report(report_obj)

                for okved_id in ctx_company.okved_ids:
                    okved_obj = CompanyOKVED(company_id=company.id, okved_id=okved_id)
                    session.add(okved_obj)

                session.commit()

        next_step(context)
