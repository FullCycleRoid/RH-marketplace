import json
from typing import List

from pipelines.generic_pipeline import Context, NextStep
from src.core.language_translator.translator import translate_large_text


class HandleAdvantagesStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:

        advantages = context.raw_company.advantages
        if advantages:
            fixed_json_string = '[' + context.raw_company.advantages.strip('{}') + ']'

            try:
                ru_advantages: List[str] = json.loads(fixed_json_string)
                ru_advantages = [item.split(": ")[1] for item in ru_advantages]
                en_advantages = [translate_large_text(adv) for adv in ru_advantages]
                print('*********** ADVANTAGES *************')
                print(ru_advantages)
                print(en_advantages)
                context.company_dto.ru_advantages = ru_advantages
                context.company_dto.en_advantages = en_advantages
                print('**************************************')
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                raise

        next_step(context)