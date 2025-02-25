from enum import Enum

class CompanyStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    SUSPENDED = 'SUSPENDED'
    ON_MODERATION = 'ON_MODERATION'

class ReportStatus(str, Enum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    VERIFIED = 'VERIFIED'
    REJECTED = 'REJECTED'

class ContactType(str, Enum):
    EMAIL = 'EMAIL'
    PHONE = 'PHONE'
    WEBSITE = 'WEBSITE'
    SOCIAL = 'SOCIAL'

class EntityType(str, Enum):
    COMPANY = 'COMPANY'
    LEGAL_FIELDS = 'LEGAL_FIELDS'
    CUSTOM_FIELD = 'CUSTOM_FIELD'
    CONTACT = 'CONTACT'
    FINANCIAL_REPORT = 'FINANCIAL_REPORT'
    TAX_REPORT = 'TAX_REPORT'
    TRANSLATION = 'TRANSLATION'

class FieldType(str, Enum):
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    DATE = 'DATE'
    BOOLEAN = 'BOOLEAN'
    ARRAY = 'ARRAY'
    OBJECT = 'OBJECT'


class FiledStatus(str, Enum):
    DRAFT = 'DRAFT'
    ACTIVATE = 'ACTIVE'
    ARCHIVED = 'ARCHIVE'


class ValidationType(str, Enum):
    REGEX = 'REGEX'
    LENGTH = 'LENGTH'
    RANGE = 'RANGE'
    CUSTOM = 'CUSTOM'