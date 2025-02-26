import re
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session

from src.company.enums import FieldType, CompanyStatus, EntityType
from src.company.models import Company, Translation
from src.company.repository import CountryLegalRequirementRepository


class CompanyService:
    def __init__(self, session: Session):
        self.session = session
        self.country_repo = CountryLegalRequirementRepository(session)

    def create_company(self, country_code: str, legal_fields: dict = None, translations: dict = None):
        # Проверяем требования для страны, если переданы поля
        if legal_fields:
            self.country_repo.validate_company_legal_fields(country_code, legal_fields)

        # Создаем компанию
        company = Company(country_code=country_code)
        self.session.add(company)
        self.session.flush()  # Получаем ID без коммита

        # Добавляем юридические поля
        if legal_fields:
            for field_name, field_info in legal_fields.items():
                field_value = field_info.get('value')
                field_type = field_info.get('type', FieldType.STRING)
                required = field_info.get('required', False)
                company.add_legal_field(field_name, field_value, field_type, required)

        # Добавляем переводы
        if translations:
            for field_name, translations_dict in translations.items():
                for lang_code, translated_value in translations_dict.items():
                    self.add_translation_to_company(company.id, field_name, lang_code, translated_value)

        self.session.commit()
        return company

    def get_company_by_id(self, company_id: UUID):
        return self.session.query(Company).filter_by(id=company_id).first()

    def update_company_status(self, company_id: UUID, new_status: CompanyStatus):
        company = self.get_company_by_id(company_id)
        if company:
            company.status = new_status
            company.updated_at = datetime.utcnow()
            self.session.commit()
            return company
        return None

    def add_legal_field_to_company(self, company_id: UUID, field_name: str, field_value: any,
                                   field_type: FieldType = FieldType.STRING, required: bool = False):
        company = self.get_company_by_id(company_id)
        if company:
            legal_field = company.add_legal_field(field_name, field_value, field_type, required)
            self.session.commit()
            return legal_field
        return None

    def add_translation_to_company(self, company_id: UUID, field_name: str, language_code: str, value: str):
        translation = Translation(
            entity_id=company_id,
            entity_type=EntityType.COMPANY,
            field_name=field_name,
            language_code=language_code,
            value=value
        )
        self.session.add(translation)
        self.session.commit()
        return translation

    def get_company_translations(self, company_id: UUID, language_code: str = None):
        query = self.session.query(Translation).filter_by(
            entity_id=company_id,
            entity_type=EntityType.COMPANY
        )
        if language_code:
            query = query.filter_by(language_code=language_code)
        return query.all()