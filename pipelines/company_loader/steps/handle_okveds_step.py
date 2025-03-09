import json

from pipelines.generic_pipeline import Context, NextStep


class HandleOKVEDSStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:

        next_step(context)