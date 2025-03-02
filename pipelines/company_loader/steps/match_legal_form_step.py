from pipelines.company_loader.utils import convert_ru_date_to_date_obj
from pipelines.generic_pipeline import Context, NextStep
from src.company.enums import LegalStatus


class MatchLegalStateStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:
        match context.raw_company.legal_entity_state:
            case "Действующая компания":
                context.company_dto.legal_status = LegalStatus.ACTIVE

            case "Действующая организация":
                context.company_dto.legal_status = LegalStatus.ACTIVE

            case status if status.startswith("Юридическое лицо ликвидировано"):
                context.company_dto.legal_status = LegalStatus.LIQUIDATED

                raw_date = status.replace("Юридическое лицо ликвидировано ", "")
                context.company_dto.liquidation_date = convert_ru_date_to_date_obj(raw_date)

            case _:
                context.company_dto.legal_status = LegalStatus.UNKNOWN

        next_step(context)