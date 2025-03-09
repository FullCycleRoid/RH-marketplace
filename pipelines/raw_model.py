from sqlalchemy import Column, DateTime, String, Integer, text as satext
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class RawCompany(Base):
    __tablename__ = "raw_chekko"

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    body = Column(String)
    name = Column(String, nullable=False)
    en_name = Column(String)
    legal_name = Column(String)
    legal_entity_state = Column(String)

    # main legal data
    inn = Column(String, nullable=False, unique=True)
    ogrn = Column(String, nullable=True, unique=True)
    kpp = Column(String)
    okpo = Column(String)
    registration_date = Column(String)
    legal_form = Column(String)
    authorized_capital = Column(String)

    annual_income = Column(String)
    net_profit = Column(String)

    taxes_paid = Column(String)
    paid_insurance = Column(String)

    # contacts and addresses
    legal_address = Column(String)

    # management
    director_name = Column(String)
    director_since = Column(String)
    average_number_of_employees = Column(String)
    sanctions = Column(String)
    reliability_assessment = Column(String)

    # process advantages
    advantages = Column(String)

    # some codes
    okogu_code = Column(String)
    okopf_code = Column(String)
    okfs_code = Column(String)
    okato_code = Column(String)
    oktmo_code = Column(String)
    code_kladr = Column(String)

    contacts = Column(JSONB)

    okved = Column(JSONB, nullable=True)

    description_of_legal_entity = Column(String)

    business_entity_section = Column(String)
    main_section = Column(String)
    rating_section = Column(String)
    detail_section = Column(String)
    contacts_section = Column(String)
    finances_section = Column(String)
    taxes_section = Column(String)
    management_section = Column(String)
    connections_section = Column(String)
    inspections_section = Column(String)

    created_at = Column(DateTime, server_default=satext("TIMEZONE('utc', now())"))
    updated_at = Column(DateTime, server_default=satext("TIMEZONE('utc', now())"), onupdate=satext("TIMEZONE('utc', now())"))
