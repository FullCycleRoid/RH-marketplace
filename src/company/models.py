import uuid
from datetime import datetime
from sqlalchemy import (Column, String, Integer, Boolean, ForeignKey, DateTime, DECIMAL, Text, Enum, func, UniqueConstraint, Index)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped
from uuid import uuid4

from src import Base
from src.company.enums import CompanyStatus, EntityType, FieldType, ValidationType, FiledStatus, ContactType, ReportStatus


class Company(Base):
    __tablename__ = 'companies'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    country_code = Column(String(2), nullable=False)
    status = Column(
        Enum(CompanyStatus, name='company_status'),
        nullable=False,
        default=CompanyStatus.ON_MODERATION
    )
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now())

    legal_fields = relationship("LegalField", back_populates="company", cascade="all, delete-orphan")
    custom_fields = relationship("CustomField", back_populates="company", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="company", cascade="all, delete-orphan")
    financial_reports = relationship("FinancialReport", back_populates="company", cascade="all, delete-orphan")
    tax_reports = relationship("TaxReport", back_populates="company", cascade="all, delete-orphan")
    change_logs = relationship("CompanyChangeLog", back_populates="company", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_company_country_code', country_code),
        Index('idx_company_status', status),
    )

    def add_legal_field(self, field_name, field_value, field_type, required=False):
        legal_field = LegalField(
            company_id=self.id,
            country_code=self.country_code,
            version=1,
            effective_from=datetime.utcnow(),
            status=FiledStatus.ACTIVE,
            modified_by=1
        )

        self.legal_fields.append(legal_field)
        legal_field_value = LegalFieldValue(
            name=field_name,
            field_type=field_type,
            value=field_value,
            required=required
        )
        legal_field.values.append(legal_field_value)
        return legal_field

    def add_contact(self, contact_type, value, metadata=None):
        contact = Contact(
            company_id=self.id,
            type=contact_type,
            value=value,
            metadata=metadata
        )
        self.contacts.append(contact)
        return contact

    def add_financial_report(self, year, annual_income, net_profit, currency):
        report = FinancialReport(
            company_id=self.id,
            year=year,
            annual_income=annual_income,
            net_profit=net_profit,
            currency=currency,
            status=ReportStatus.DRAFT
        )
        self.financial_reports.append(report)
        return report

    def add_tax_report(self, year, quarter, period_start, period_end):
        report = TaxReport(
            company_id=self.id,
            year=year,
            quarter=quarter,
            period_start=period_start,
            period_end=period_end,
            status=ReportStatus.DRAFT
        )
        self.tax_reports.append(report)
        return report


class Translation(Base):
    __tablename__ = 'translations'

    id: Mapped[UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False)
    entity_type: Mapped[EntityType] = Column(Enum(EntityType), nullable=False)
    field_name: Mapped[str] = Column(String(255), nullable=False)
    language_code: Mapped[str] = Column(String(2), nullable=False)
    value: Mapped[str] = Column(Text, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('entity_id', 'entity_type', 'field_name', 'language_code', name='uq_translation'),
    )


class CountryLegalRequirement(Base):
    __tablename__ = 'country_legal_requirements'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    country_code = Column(String(2), nullable=False)
    version = Column(String(50), nullable=False)
    active_from = Column(DateTime(timezone=True), nullable=False)
    active_to = Column(DateTime(timezone=True))
    status = Column(Enum(FiledStatus, name='field_status'), nullable=False)

    # Отношения
    required_fields = relationship("RequiredField", back_populates="requirement", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('country_code', 'version', name='uq_country_version'),
        Index('idx_country_legal_req_country', country_code),
        Index('idx_country_legal_req_status', status)
    )


# Требуемые поля для стран
class RequiredField(Base):
    __tablename__ = 'required_fields'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    requirement_id = Column(UUID(as_uuid=True), ForeignKey('country_legal_requirements.id'), nullable=False)
    name = Column(String(255), nullable=False)
    field_type = Column(Enum(FieldType, name='field_type'), nullable=False)
    display_order = Column(Integer, nullable=False)

    # Отношения
    requirement = relationship("CountryLegalRequirement", back_populates="required_fields")
    validation_rules = relationship("ValidationRule", back_populates="field", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('requirement_id', 'name', name='uq_required_field'),
        Index('idx_required_field_req_id', requirement_id)
    )


# Правила валидации для требуемых полей
class ValidationRule(Base):
    __tablename__ = 'validation_rules'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey('required_fields.id'), nullable=False)
    validation_type = Column(Enum(ValidationType, name='validation_type'), nullable=False)
    params = Column(JSONB, nullable=False)
    error_code = Column(String(50), nullable=False)

    # Отношения
    field = relationship("RequiredField", back_populates="validation_rules")


# Юридические поля компаний
class LegalField(Base):
    __tablename__ = 'legal_fields'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    country_code = Column(String(2), nullable=False)
    version = Column(Integer, nullable=False)
    effective_from = Column(DateTime(timezone=True), nullable=False)
    effective_to = Column(DateTime(timezone=True))
    modified_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('users.id'))
    previous_version = Column(UUID(as_uuid=True), ForeignKey('legal_fields.id'))
    change_reason = Column(Text)
    status = Column(Enum(FiledStatus, name='field_status'), nullable=False)
    is_translatable = Column(Boolean, nullable=False, default=False)

    # Отношения
    company = relationship("Company", back_populates="legal_fields")
    values = relationship("LegalFieldValue", back_populates="legal_field", cascade="all, delete-orphan")
    previous = relationship("LegalField", remote_side=[id], backref="next_versions")


# Значения юридических полей
class LegalFieldValue(Base):
    __tablename__ = 'legal_field_values'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    legal_fields_id = Column(UUID(as_uuid=True), ForeignKey('legal_fields.id'), nullable=False)
    name = Column(String(255), nullable=False)
    field_type = Column(Enum(FieldType, name='field_type'), nullable=False)
    value = Column(JSONB, nullable=False)
    required = Column(Boolean, nullable=False, default=False)

    # Отношения
    legal_field = relationship("LegalField", back_populates="values")


# Пользовательские поля
class CustomField(Base):
    __tablename__ = 'custom_fields'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    name = Column(String(255), nullable=False)
    field_type = Column(Enum(FieldType, name='field_type'), nullable=False)
    value = Column(JSONB, nullable=False)
    is_translatable = Column(Boolean, nullable=False, default=False)

    # Отношения
    company = relationship("Company", back_populates="custom_fields")


# Контакты компаний
class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    type = Column(Enum(ContactType, name='contact_type'), nullable=False)
    value = Column(Text, nullable=False)
    metadata = Column(JSONB)
    is_verified = Column(Boolean, nullable=False, default=False)
    verified_at = Column(DateTime(timezone=True))

    # Отношения
    company = relationship("Company", back_populates="contacts")


# Финансовые отчеты
class FinancialReport(Base):
    __tablename__ = 'financial_reports'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    year = Column(Integer, nullable=False)
    annual_income = Column(DECIMAL(20, 2), nullable=False)
    net_profit = Column(DECIMAL(20, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    status = Column(Enum(ReportStatus, name='report_status'), nullable=False)
    audited_by = Column(Integer, ForeignKey('users.id'))

    # Отношения
    company = relationship("Company", back_populates="financial_reports")


# Налоговые отчеты
class TaxReport(Base):
    __tablename__ = 'tax_reports'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(ReportStatus, name='report_status'), nullable=False)

    # Отношения
    company = relationship("Company", back_populates="tax_reports")


# Аудит изменений
class CompanyChangeLog(Base):
    __tablename__ = 'company_change_log'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    entity_type = Column(Enum(EntityType, name='entity_type'), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reason = Column(Text)
    changes = Column(JSONB, nullable=False)

    # Отношения
    company = relationship("Company", back_populates="change_logs")
