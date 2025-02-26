import re
from datetime import datetime
from uuid import UUID

from requests import Session
from sqlalchemy import or_

from src.company.enums import FiledStatus, ValidationType, FieldType, CompanyStatus, EntityType
from src.company.models import Company, CountryLegalRequirement, ValidationRule, Translation


class CountryLegalRequirementRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_active_country_requirements(self, country_code: str, target_date: datetime = None):
        if not target_date:
            target_date = datetime.utcnow()

        return self.session.query(CountryLegalRequirement).filter(
            CountryLegalRequirement.country_code == country_code,
            CountryLegalRequirement.active_from <= target_date,
            or_(
                CountryLegalRequirement.active_to.is_(None),
                CountryLegalRequirement.active_to >= target_date
            ),
            CountryLegalRequirement.status == FiledStatus.ACTIVE
        ).first()

    def get_country_requirements(self, country_code: str, version: str = None):
        query = self.session.query(CountryLegalRequirement).filter_by(country_code=country_code)
        if version:
            query = query.filter_by(version=version)
        else:
            # Если версия не указана, возвращаем активную версию
            return self.get_active_country_requirements(country_code)
        return query.first()

    def validate_company_legal_fields(self, company_country_code: str, legal_fields: dict):
        requirements = self.get_active_country_requirements(company_country_code)
        if not requirements:
            raise ValueError(f"No active legal requirements found for country code: {company_country_code}")

        required_fields = {rf.name: rf for rf in requirements.required_fields}

        # Проверяем, что все обязательные поля присутствуют
        for field_name, required_field in required_fields.items():
            if field_name not in legal_fields and required_field.is_required:
                raise ValueError(f"Required field '{field_name}' is missing.")

        # Валидируем переданные поля
        for field_name, field_info in legal_fields.items():
            if field_name not in required_fields:
                raise ValueError(f"Field '{field_name}' is not defined for this country.")

            required_field = required_fields[field_name]
            field_value = field_info.get('value') if isinstance(field_info, dict) else field_info

            for rule in required_field.validation_rules:
                self._validate_rule(rule, field_value)

    def _validate_rule(self, rule: ValidationRule, value):
        if rule.validation_type == ValidationType.LENGTH:
            length = rule.params.get("length")
            if len(str(value)) != length:
                raise ValueError(f"Value '{value}' does not meet the length requirement of {length}.")
        elif rule.validation_type == ValidationType.REGEX:
            pattern = rule.params.get("pattern")
            if not re.match(pattern, str(value)):
                raise ValueError(f"Value '{value}' does not match the regex pattern: {pattern}.")
        # Добавьте другие типы валидации по необходимости


class CompanyRepository:
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