from pipelines.company_loader.utils import convert_ru_date_to_date_obj
from pipelines.generic_pipeline import Context, NextStep
from src.core.logger import logger


class ConvertRegistrationDateStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:
        registration_date = context.raw_company.registration_date

        if not registration_date:
            logger.info("Registration date is None")
        else:
            context.company_dto.registration_date = convert_ru_date_to_date_obj(registration_date)

        next_step(context)
