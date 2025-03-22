import uuid
from typing import Dict

from sqlalchemy.orm import Session

from pipelines.company_loader.context import CompanyDTO
from pipelines.connector import MarketplaceDBSession
from pipelines.generic_pipeline import Context, NextStep
from src import Company
from src.company.enums import TranslationMode


class BuildCompanyDBModel:
    def __init__(self, session: Session = MarketplaceDBSession):
        self.session = session

    def __call__(self, context: Context, next_step: NextStep) -> None:
        with self.session() as session:
            ctx_company: CompanyDTO = context.company_dto
            field_type_ids: Dict[str, uuid] = context.field_type_ids


            company = Company(
                country_code=ctx_company.country_code,
                legal_status=ctx_company.legal_status,
                system_status=ctx_company.system_status,
            )

            for name, type_id in field_type_ids.items():
                if name == 'name':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.name,
                        en_data=ctx_company.en_name,
                        is_translatable=True,
                        translation_type=TranslationMode.AUTO
                    )
                if name == 'legal_name':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.legal_name,
                        en_data=ctx_company.en_legal_name,
                        is_translatable=True,
                        translation_type=TranslationMode.AUTO
                    )
                if name == 'inn':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.inn,
                        en_data=ctx_company.inn,
                        is_translatable=False,
                    )
                if name == 'ogrn':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.ogrn,
                        en_data=ctx_company.ogrn,
                        is_translatable=False,
                    )
                if name == 'kpp':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.kpp,
                        en_data=ctx_company.kpp,
                        is_translatable=False,
                    )
                if name == 'okpo':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.okpo,
                        en_data=ctx_company.okpo,
                        is_translatable=False,
                    )
                if name == 'okogu_code':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.okogu_code,
                        en_data=ctx_company.okogu_code,
                        is_translatable=False,
                    )
                if name == 'okopf_code':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.okopf_code,
                        en_data=ctx_company.okopf_code,
                        is_translatable=False,
                    )
                if name == 'okfs_code':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.okfs_code,
                        en_data=ctx_company.okfs_code,
                        is_translatable=False,
                    )
                if name == 'okato_code':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.okato_code,
                        en_data=ctx_company.okato_code,
                        is_translatable=False,
                    )
                if name == 'oktmo_code':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.oktmo_code,
                        en_data=ctx_company.oktmo_code,
                        is_translatable=False,
                    )
                if name == 'kladr_code':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.code_kladr,
                        en_data=ctx_company.code_kladr,
                        is_translatable=False,
                    )
                if name == 'registration_date':
                    company.add_field(
                        company_field_type_id=type_id,
                        datetime_data=ctx_company.registration_date,
                        is_translatable=False,
                    )
                if name == 'liquidation_date':
                    company.add_field(
                        company_field_type_id=type_id,
                        datetime_data=ctx_company.liquidation_date,
                        is_translatable=False,
                    )
                if name == 'authorized_capital':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.authorized_capital,
                        en_data=ctx_company.authorized_capital,
                        is_translatable=False,
                    )
                if name == 'average_number_of_employees':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.average_number_of_employees,
                        en_data=ctx_company.average_number_of_employees,
                        is_translatable=False,
                    )

                if name == 'advantages':
                    ru_advantages = ', '.join(ctx_company.advantages)
                    en_advantages = ', '.join(ctx_company.en_advantages)
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ru_advantages,
                        en_data=en_advantages,
                        is_translatable=True,
                        translation_type=TranslationMode.AUTO
                    )

            for contact in ctx_company.contacts:
                company.add_contact(
                    type=contact.type,
                    date=contact.value,
                    is_verified=contact.is_verified
                )

            for manager in ctx_company.managers:
                company.add_manager(**manager)

            for report in ctx_company.tax_reports:
                company.add_tax_report(**report)

            for report in ctx_company.financial_reports:
                company.add_financial_report(**report)
            session.add(company)
            session.commit()
        next_step(context)


