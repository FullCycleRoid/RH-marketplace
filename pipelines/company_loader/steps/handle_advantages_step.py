import json
from typing import List

from pipelines.generic_pipeline import Context, NextStep
from pipelines.utils import get_random_proxy_obj
from src.core.language_translator.proxy_google_translator2 import translate_large_text


class HandleAdvantagesStep:
    def __init__(self, translator=None):
        self.translator = translator

    def __call__(self, context: Context, next_step: NextStep) -> None:
        advantages = context.raw_company.advantages

        if advantages:
            fixed_json_string = "[" + context.raw_company.advantages.strip("{}") + "]"

            try:
                ru_advantages: List[str] = json.loads(fixed_json_string)
                ru_advantages = [item.split(": ")[1] for item in ru_advantages]

                en_advantages = []

                for adv in ru_advantages:
                    print(adv)
                    if adv in context.translated_advantages:
                        en_adv = context.translated_advantages[adv]

                    if adv not in context.translated_advantages:
                        en_adv = (
                            translate_large_text(
                                adv, proxy_obj=get_random_proxy_obj(context.proxies)
                            ),
                        )

                        if isinstance(en_adv, tuple):
                            en_adv = en_adv[0]
                        context.translated_advantages[adv] = en_adv

                    if isinstance(en_adv, tuple):
                        en_adv = en_adv[0]
                    en_advantages.append(en_adv)

                print("*********** ADVANTAGES *************")
                print(ru_advantages)
                print(en_advantages)
                context.company_dto.ru_advantages = ru_advantages
                context.company_dto.en_advantages = en_advantages
                print("**************************************")

            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                raise

        next_step(context)
