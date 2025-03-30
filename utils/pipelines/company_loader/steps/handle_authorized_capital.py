import re

from utils.pipelines.generic_pipeline import Context, NextStep, PipelineStep
from src.core.logger import logger


class ConvertAuthorizedCapitalStep(PipelineStep):
    def __call__(self, context: Context, next_step: NextStep) -> None:
        raw_data = context.raw_company.authorized_capital

        if raw_data:
            clean_data = int("".join(re.findall(r"\d", raw_data)))
            if not clean_data:
                logger.info("Authorized capital is None")
            else:
                context.company_dto.authorized_capital = clean_data
        next_step(context)
