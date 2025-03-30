from utils.pipelines.generic_pipeline import Context, NextStep, PipelineStep
from utils.pipelines.utils import convert_ru_date_to_date_obj
from src.company.enums import LegalStatus


class MatchLegalStateStep(PipelineStep):
    def __call__(self, context: Context, next_step: NextStep) -> None:
        legal_entity_state = context.raw_company.legal_entity_state

        if legal_entity_state == "Действующая компания":
            context.company_dto.legal_status = LegalStatus.ACTIVE

        elif legal_entity_state == "Действующий ИП":
            context.company_dto.legal_status = LegalStatus.ACTIVE

        elif legal_entity_state == "Действующая организация":
            context.company_dto.legal_status = LegalStatus.ACTIVE

        elif legal_entity_state.startswith("Юридическое лицо ликвидировано"):
            context.company_dto.legal_status = LegalStatus.LIQUIDATED
            raw_date = legal_entity_state.replace("Юридическое лицо ликвидировано ", "")
            context.company_dto.liquidation_date = convert_ru_date_to_date_obj(raw_date)

        elif legal_entity_state.startswith("Не действует с"):
            context.company_dto.legal_status = LegalStatus.LIQUIDATED
            raw_date = legal_entity_state.replace("Не действует с ", "")
            context.company_dto.liquidation_date = convert_ru_date_to_date_obj(raw_date)

        elif "исключении" in legal_entity_state:
            context.company_dto.legal_status = LegalStatus.EXCLUDED_FROM_REGISTER

        elif "банкрот" in legal_entity_state:
            context.company_dto.legal_status = LegalStatus.BANKRUPTCY

        else:
            context.company_dto.legal_status = LegalStatus.UNKNOWN

        next_step(context)
