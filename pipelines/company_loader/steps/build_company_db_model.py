from typing import List

from pipelines.company_loader.context import CompanyDTO
from pipelines.generic_pipeline import Context, NextStep
from src import Company, CompanyField
from src.core.logger import logger


class BuildCompanyDBModel:
    def __call__(self, context: Context, next_step: NextStep) -> None:

        ctx_company: CompanyDTO = context.company_dto
        field_types: List[CompanyField] = context.field_types

        company = Company(
            country_code=ctx_company.country_code,
            legal_status=ctx_company.legal_status,
            system_status=ctx_company.system_status,
        )

        # name_field


        next_step(context)
