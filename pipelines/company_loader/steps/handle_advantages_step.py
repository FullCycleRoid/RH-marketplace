import json
from typing import List

from pipelines.generic_pipeline import Context, NextStep, PipelineStep


class HandleAdvantagesStep(PipelineStep):
    def __init__(self, translator=None):
        self.translator = translator

    def __call__(self, context: Context, next_step: NextStep) -> None:
        advantages = context.raw_company.advantages

        if advantages:
            fixed_json_string = "[" + context.raw_company.advantages.strip("{}") + "]"

            try:
                ru_advantages: List[str] = json.loads(fixed_json_string)
                ru_advantages = [item.split(": ")[1] for item in ru_advantages]

                print("*********** ADVANTAGES *************")
                context.company_dto.advantages.extend(ru_advantages)
                print("**************************************")

            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                raise

        next_step(context)
