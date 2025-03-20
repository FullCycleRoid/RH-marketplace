import re

from pipelines.generic_pipeline import Context, NextStep
from src.core.logger import logger


class BuildCompanyDBModel:
    def __call__(self, context: Context, next_step: NextStep) -> None:



        next_step(context)
