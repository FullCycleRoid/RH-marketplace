from sqlalchemy import (Column, String, Integer, Boolean, ForeignKey, DateTime, DECIMAL, Text, Enum, func,
                        UniqueConstraint, Index, DDL)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship
from uuid import uuid4

from src import Base
from src.company.enums import LegalStatus, EntityType, FieldType, ValidationType, FiledStatus, ContactType, ReportStatus, SystemStatus, \
    TranslationType, ManagerType


class Company(Base):
    __tablename__ = 'companies'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    country_code = Column(String(2), nullable=False)
    legal_status = Column(
        Enum(LegalStatus, name='legal_status'),
        nullable=False,
        default=LegalStatus.UNKNOWN
    )
    system_status = Column(
        Enum(SystemStatus, name='system_status'),
        nullable=False,
        default=LegalStatus.ON_MODERATION
    )
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now())

    legal_fields = relationship("LegalField", back_populates="company", cascade="all, delete-orphan")
    system_fields = relationship("SystemField", back_populates="company", cascade="all, delete-orphan")
    custom_fields = relationship("CustomField", back_populates="company", cascade="all, delete-orphan")

    contacts = relationship("Contact", back_populates="company", cascade="all, delete-orphan")
    managers = relationship("Manager", back_populates="company", cascade="all, delete-orphan")

    financial_reports = relationship("FinancialReport", back_populates="company", cascade="all, delete-orphan")
    tax_reports = relationship("TaxReport", back_populates="company", cascade="all, delete-orphan")

    change_logs = relationship("CompanyChangeLog", back_populates="company", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_company_country_code', country_code),
        Index('idx_legal_status', legal_status),
    )

    def add_legal_field(self, field_name, field_value, field_type, required=False):
        legal_field = LegalField(
            name=field_name,
            field_type=field_type,
            value=field_value,
            required=required
        )
        self.legal_fields.append(legal_field)
        return legal_field

    def add_contact(self, contact_type, value):
        contact = Contact(
            company_id=self.id,
            type=contact_type,
            value=value
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


class CompanyOKVED(Base):
    __tablename__ = 'company_m2m_okved'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    okved_id = Column(Integer, ForeignKey('okved_nodes.id'), nullable=False)


class CountryLegalRequirement(Base):
    __tablename__ = 'country_legal_requirements'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    country_code = Column(String(2), nullable=False)
    version = Column(String(50), nullable=False)
    active_from = Column(DateTime(timezone=True), nullable=False)
    active_to = Column(DateTime(timezone=True))
    status = Column(Enum(FiledStatus, name='field_status'), nullable=False)

    required_fields = relationship("RequiredField", back_populates="requirement", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('country_code', 'version', name='uq_country_version'),
        Index('idx_country_legal_req_country', country_code),
        Index('idx_country_legal_req_status', status)
    )


class RequiredField(Base):
    __tablename__ = 'required_fields'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    requirement_id = Column(UUID(as_uuid=True), ForeignKey('country_legal_requirements.id'), nullable=False)
    name = Column(String(255), nullable=False)

    field_type = Column(Enum(FieldType, name='field_type'), nullable=False)
    display_order = Column(Integer, nullable=False)

    requirement = relationship("CountryLegalRequirement", back_populates="required_fields")
    validation_rules = relationship("ValidationRule", back_populates="field", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('requirement_id', 'name', name='uq_required_field'),
        Index('idx_required_field_req_id', requirement_id)
    )


class ValidationRule(Base):
    __tablename__ = 'validation_rules'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey('required_fields.id'), nullable=False)
    validation_type = Column(Enum(ValidationType, name='validation_type'), nullable=False)
    params = Column(JSONB, nullable=False)
    error_code = Column(String(50), nullable=False)

    # Отношения
    field = relationship("RequiredField", back_populates="validation_rules")


class LegalField(Base):
    __tablename__ = 'legal_fields'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    name = Column(String(255), nullable=False)

    field_type = Column(Enum(FieldType, name='field_type'), nullable=False)
    value = Column(JSONB, nullable=True)

    required = Column(Boolean, nullable=False, default=False)
    is_translatable = Column(Boolean, nullable=False, default=False)
    translation_type = Column(Enum(TranslationType, name='translation_type'), nullable=True, default=True)

    company = relationship("Company", back_populates="legal_fields")


class SystemField(Base):
    __tablename__ = 'system_fields'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    name = Column(String(255), nullable=False)

    field_type = Column(Enum(FieldType, name='field_type'), nullable=False)
    value = Column(JSONB, nullable=True)

    is_translatable = Column(Boolean, nullable=False, default=False)
    translation_type = Column(Enum(TranslationType, name='translation_type'), nullable=True, default=True)

    company = relationship("Company", back_populates="system_fields")


class CustomField(Base):
    __tablename__ = 'custom_fields'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    name = Column(String(255), nullable=False)

    field_type = Column(Enum(FieldType, name='field_type'), nullable=False)
    value = Column(JSONB, nullable=True)

    is_translatable = Column(Boolean, nullable=False, default=False)
    translation_type = Column(Enum(TranslationType, name='translation_type'), nullable=True, default=True)

    company = relationship("Company", back_populates="custom_fields")


class Manager(Base):
    __tablename__ = 'managers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)

    position = Column(Enum(ManagerType, name='manager_type'), nullable=False)
    inn = Column(Text, nullable=True)

    full_name = Column(Text, nullable=True)
    en_full_name = Column(Text, nullable=True)

    since_on_position = Column(DateTime(timezone=True), nullable=True)

    company = relationship("Company", back_populates="managers")


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    type = Column(Enum(ContactType, name='contact_type'), nullable=False)
    value = Column(Text, nullable=False)

    is_verified = Column(Boolean, nullable=False, default=False)

    company = relationship("Company", back_populates="contacts")


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

    company = relationship("Company", back_populates="financial_reports")


class TaxReport(Base):
    __tablename__ = 'tax_reports'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(ReportStatus, name='report_status'), nullable=False)

    company = relationship("Company", back_populates="tax_reports")


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

    company = relationship("Company", back_populates="change_logs")


create_enum_type = DDL("CREATE TYPE translation_type AS ENUM ('manual', 'automatic');")
listen(LegalField.__table__, 'before_create', create_enum_type.execute_if(dialect='postgresql'))