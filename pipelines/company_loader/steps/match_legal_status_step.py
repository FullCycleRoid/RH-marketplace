from pipelines.utils import convert_ru_date_to_date_obj
from pipelines.generic_pipeline import Context, NextStep
from src.company.enums import LegalStatus


class MatchLegalStateStep:
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


# from pipelines.utils import convert_ru_date_to_date_obj
# from pipelines.generic_pipeline import Context, NextStep
# from src.company.enums import LegalStatus
#
#
# class MatchLegalStateStep:
#     def __call__(self, context: Context, next_step: NextStep) -> None:
#         match context.raw_company.legal_entity_state:
#             case "Действующая компания":
#                 context.company_dto.legal_status = LegalStatus.ACTIVE
#
#             case "Действующий ИП":
#                 context.company_dto.legal_status = LegalStatus.ACTIVE
#
#             case "Действующая организация":
#                 context.company_dto.legal_status = LegalStatus.ACTIVE
#
#             case status if status.startswith("Юридическое лицо ликвидировано"):
#                 context.company_dto.legal_status = LegalStatus.LIQUIDATED
#
#                 raw_date = status.replace("Юридическое лицо ликвидировано ", "")
#                 context.company_dto.liquidation_date = convert_ru_date_to_date_obj(raw_date)
#
#             case status if status.startswith("Не действует с"):
#                 context.company_dto.legal_status = LegalStatus.LIQUIDATED
#
#                 raw_date = status.replace("Не действует с ", "")
#                 context.company_dto.liquidation_date = convert_ru_date_to_date_obj(raw_date)
#
#             case status if "исключении" in status:
#                 context.company_dto.legal_status = LegalStatus.EXCLUDED_FROM_REGISTER
#
#             case status if "банкрот" in status:
#                 context.company_dto.legal_status = LegalStatus.BANKRUPTCY
#
#             case _:
#                 context.company_dto.legal_status = LegalStatus.UNKNOWN
#
#         next_step(context)