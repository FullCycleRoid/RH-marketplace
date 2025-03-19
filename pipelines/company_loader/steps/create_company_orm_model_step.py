from pipelines.generic_pipeline import Context, NextStep
from src.company.infrastructure.models import Company


class CreateCompanyORMStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:

        company_orm = Company(
            country_code='RU',

        )
