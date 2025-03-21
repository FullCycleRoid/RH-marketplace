import uuid
from typing import Dict

from sqlalchemy.orm import Session

from pipelines.company_loader.context import CompanyDTO
from pipelines.connector import MarketplaceDBSession
from pipelines.generic_pipeline import Context, NextStep
from src import Company
from src.company.enums import TranslationType


class BuildCompanyDBModel:
    def __init__(self, session: Session = MarketplaceDBSession):
        self.session = session

    def __call__(self, context: Context, next_step: NextStep) -> None:
        with self.session() as session:
            ctx_company: CompanyDTO = context.company_dto
            field_type_ids: Dict[str, uuid] = context.field_type_ids
            translation_config = {
                "is_translatable": True,
                "translation_type": TranslationType.AUTO
            }

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
                        translation_config=translation_config
                    )
                if name == 'legal_name':
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.legal_name,
                        en_data=ctx_company.en_legal_name,
                        translation_config=translation_config
                    )
                if name == 'inn':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.inn,
                        en_data=ctx_company.inn,
                        translation_config=translation_config
                    )
                if name == 'ogrn':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.ogrn,
                        en_data=ctx_company.ogrn,
                        translation_config=translation_config
                    )
                if name == 'kpp':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.kpp,
                        en_data=ctx_company.kpp,
                        translation_config=translation_config
                    )
                if name == 'okpo':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.okpo,
                        en_data=ctx_company.okpo,
                        translation_config=translation_config
                    )
                if name == 'okogu_code':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.okogu_code,
                        en_data=ctx_company.okogu_code,
                        translation_config=translation_config
                    )
                if name == 'okopf_code':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.okopf_code,
                        en_data=ctx_company.okopf_code,
                        translation_config=translation_config
                    )
                if name == 'okfs_code':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.okfs_code,
                        en_data=ctx_company.okfs_code,
                        translation_config=translation_config
                    )
                if name == 'okato_code':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.okato_code,
                        en_data=ctx_company.okato_code,
                        translation_config=translation_config
                    )
                if name == 'oktmo_code':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.oktmo_code,
                        en_data=ctx_company.oktmo_code,
                        translation_config=translation_config
                    )
                if name == 'kladr_code':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.code_kladr,
                        en_data=ctx_company.code_kladr,
                        translation_config=translation_config
                    )
                if name == 'registration_date':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        datetime_data=ctx_company.registration_date,
                        translation_config=translation_config
                    )
                if name == 'liquidation_date':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        datetime_data=ctx_company.liquidation_date,
                        translation_config=translation_config
                    )
                if name == 'authorized_capital':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.authorized_capital,
                        en_data=ctx_company.authorized_capital,
                        translation_config=translation_config
                    )
                if name == 'average_number_of_employees':
                    translation_config = {"is_translatable": False}
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ctx_company.average_number_of_employees,
                        en_data=ctx_company.average_number_of_employees,
                        translation_config=translation_config
                    )

                if name == 'advantages':
                    ru_advantages = ', '.join(ctx_company.advantages)
                    en_advantages = ', '.join(ctx_company.en_advantages)
                    company.add_field(
                        company_field_type_id=type_id,
                        ru_data=ru_advantages,
                        en_data=en_advantages,
                        translation_config=translation_config
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


