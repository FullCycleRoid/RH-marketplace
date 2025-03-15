import json

from pipelines.generic_pipeline import Context, NextStep


class HandleAdvantagesStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:
        fixed_json_string = '[' + context.raw_company.advantages.strip('{}') + ']'

        try:
            loaded = json.loads(fixed_json_string)
            context.company_dto.advantages = loaded
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            raise

        next_step(context)