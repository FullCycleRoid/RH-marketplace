from requests import Session

from pipelines.company_loader.connector import SessionFactory
from pipelines.company_loader.raw_model import RawCompany
from pipelines.generic_pipeline import Context, NextStep
from src.company.models import Company


class CreateCompanyORMStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:

        company_orm = Company(
            country_code='RU',

        )
