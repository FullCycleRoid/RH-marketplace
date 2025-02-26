# Создание подключения к базе данных
```json
engine = create_engine('postgresql://user:password@localhost/dbname')
Session = sessionmaker(bind=engine)
session = Session()
```

# Создание репозитория
```json
repository = CompanyRepository(session)
```

# Создание новой компании с обязательными полями
```json
legal_fields = {
    "INN": {"value": "1234567890", "type": FieldType.STRING, "required": True},
    "OGRN": {"value": "1234567890123", "type": FieldType.STRING, "required": True},
    "KPP": {"value": "123456789", "type": FieldType.STRING, "required": True},
    "NAME": {"value": "My Company", "type": FieldType.STRING, "required": True},
    "LEGAL_NAME": {"value": "My Legal Company", "type": FieldType.STRING, "required": True}
}

translations = {
    "NAME": {"en": "My Company", "ru": "Моя Компания"},
    "LEGAL_NAME": {"en": "My Legal Company", "ru": "Моя Юридическая Компания"}
}

new_company = repository.create_company(
    country_code="RU",
    legal_fields=legal_fields,
    translations=translations
)
```

# Добавление контактов
```json
repository.add_contact_to_company(new_company.id, ContactType.EMAIL, "info@example.com")
repository.add_contact_to_company(new_company.id, ContactType.PHONE, "+71234567890")
```

# Добавление финансового отчета
```json
repository.add_financial_report_to_company(new_company.id, 2023, 1000000, 200000, "RUB")
```

# Добавление налогового отчета
```json
repository.add_tax_report_to_company(
    new_company.id, 
    2023, 
    1, 
    datetime(2023, 1, 1), 
    datetime(2023, 3, 31)
)
```