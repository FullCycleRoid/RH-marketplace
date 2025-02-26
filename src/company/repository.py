import re
from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.company.enums import FiledStatus, ValidationType
from src.company.models import CountryLegalRequirement, ValidationRule


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
