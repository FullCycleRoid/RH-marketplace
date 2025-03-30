from src.core.database.postgres.session_manager import DatabaseSessionManager
from src.core.logger import logger

from pipelines.generic_pipeline import Context, NextStep, PipelineStep
from pipelines.utils import get_company_by_inn
from src import (Company, CompanyOKVED, FinancialReport,
                 TaxReport, FieldTranslation, Manager, ManagerTranslation, Contact)
from src.company.enums import TranslationMode


class BuildCompanyDBModelStep(PipelineStep):
    _sessionmaker = None

    @classmethod
    def get_sessionmaker(cls):
        if cls._sessionmaker is None:
            cls._sessionmaker = DatabaseSessionManager.get_sessionmaker()
        return cls._sessionmaker

    def __call__(self, context: Context, next_step: NextStep) -> None:
        with self.get_sessionmaker()() as session:
            ctx_company = context.company_dto

            if not get_company_by_inn(session, ctx_company.inn):
                company = Company(
                    country_code=ctx_company.country_code,
                    legal_status=ctx_company.legal_status,
                    system_status=ctx_company.system_status,
                )
                session.add(company)
                session.flush()

                # Добавление русского перевода для компании
                if ctx_company.name:
                    company.add_translation(
                        language_code="RU",
                        name=ctx_company.name,
                    )

                if ctx_company.en_name:
                    company.add_translation(
                        language_code="EN",
                        name=ctx_company.en_name,
                    )

            # Маппинг полей компании
                fields_config = {
                    'legal_name': (ctx_company.legal_name, 'STRING'),
                    'legal_description': (ctx_company.legal_description, 'STRING'),
                    'inn': (ctx_company.inn, 'CODE'),
                    'registration_date': (ctx_company.registration_date, 'DATE'),
                    'liquidation_date': (ctx_company.liquidation_date, 'DATE'),
                    'legal_address': (ctx_company.legal_address, 'STRING'),
                    'ogrn': (ctx_company.ogrn, 'CODE'),
                    'kpp': (ctx_company.kpp, 'CODE'),
                    'okpo': (ctx_company.okpo, 'CODE'),
                    'authorized_capital': (ctx_company.authorized_capital, 'STRING'),
                    'average_number_of_employees': (ctx_company.average_number_of_employees, 'STRING'),
                    'okogu_code': (ctx_company.okogu_code, 'CODE'),
                    'okopf_code': (ctx_company.okopf_code, 'CODE'),
                    'okfs_code': (ctx_company.okfs_code, 'CODE'),
                    'okato_code': (ctx_company.okato_code, 'CODE'),
                    'oktmo_code': (ctx_company.oktmo_code, 'CODE'),
                    'kladr_code': (ctx_company.code_kladr, 'CODE'),
                    'advantages': (ctx_company.ready_advantages, 'STRING'),
                }

                for field_name, (value, data_type) in fields_config.items():
                    if value is None or value == '' or value == (' '
                                                                 ''):
                        continue

                    field_type_id = context.field_type_ids.get(field_name)
                    if not field_type_id:
                        continue

                    try:
                        # Создаем поле
                        field = company.add_field(
                            company_field_type_id=field_type_id,
                            is_translatable=True,
                            translation_mode=TranslationMode.AUTO
                        )

                        # Добавляем русский перевод
                        if data_type == 'STRING':
                            field.translations.append(
                                FieldTranslation(
                                    language_code='RU',
                                    data=str(value)
                                )
                            )
                        elif data_type == 'DATE':
                            field.datetime_data = value
                        elif data_type == 'CODE':
                            field.code = value
                        elif data_type == 'ARRAY':
                            field.json_data = {'data': list(value)}

                    except Exception as e:
                        logger.error(f"Ошибка добавления поля {field_name}: {str(e)}")
                        context.failed_records += 1

                for contact in ctx_company.contacts:
                    contact_obj = Contact(
                        type=contact.type,
                        data=contact.value,
                        is_verified=contact.is_verified,
                    )
                    company.add_contact(contact_obj)

                # Добавление менеджеров
                for manager_dto in ctx_company.management:
                    try:
                        manager = Manager(
                            position=manager_dto.position,
                            inn=manager_dto.inn,
                            since_on_position=manager_dto.since_on_position
                        )

                        # Добавляем русский перевод ФИО
                        manager.translations.append(
                            ManagerTranslation(
                                language_code='RU',
                                full_name=manager_dto.full_name
                            )
                        )

                        company.managers.append(manager)
                    except Exception as e:
                        logger.error(f"Ошибка добавления менеджера: {str(e)}")
                        context.failed_records += 1

                # Финансовые отчеты
                for report in ctx_company.financial_reports:
                    try:
                        financial_report = FinancialReport(
                            year=report.year,
                            annual_income=report.annual_income,
                            net_profit=report.net_profit,
                            currency=report.currency
                        )
                        company.financial_reports.append(financial_report)
                    except Exception as e:
                        logger.error(f"Ошибка финансового отчета: {str(e)}")
                        context.failed_records += 1

                # Налоговые отчеты
                for report in ctx_company.tax_reports:
                    try:
                        tax_report = TaxReport(
                            year=report.year,
                            taxes_paid=report.taxes_paid,
                            paid_insurance=report.paid_insurance
                        )
                        company.tax_reports.append(tax_report)
                    except Exception as e:
                        logger.error(f"Ошибка налогового отчета: {str(e)}")
                        context.failed_records += 1

                # Привязка OKVED кодов
                for okved_id in ctx_company.okved_ids:
                    try:
                        okved_obj = CompanyOKVED(company_id=company.id, okved_id=okved_id)
                        session.add(okved_obj)
                    except Exception as e:
                        logger.error(f"Ошибка привязки OKVED: {str(e)}")
                        context.failed_records += 1
                try:
                    session.commit()
                except Exception as e:
                    logger.error(f"Ошибка коммита: {str(e)}")
                    session.rollback()
                    context.failed_records += 1

        next_step(context)