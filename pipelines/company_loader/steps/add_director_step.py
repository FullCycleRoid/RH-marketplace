from pipelines.company_loader.dto import Manager
from pipelines.generic_pipeline import Context, NextStep, PipelineStep
from pipelines.utils import convert_ru_date_to_date_obj
from src.company.enums import ManagerType


def extract_inn_by_director(text, director_name):
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    for i, line in enumerate(lines):
        if director_name in line:
            if i + 1 < len(lines) and lines[i + 1].startswith("ИНН"):
                inn_line =  lines[i + 1]
                separated = inn_line.split(" ")
                if len(separated) == 2:
                    inn = separated[1]
                    return inn

    return None


class AddDirectorStep(PipelineStep):
    def __call__(self, context: Context, next_step: NextStep) -> None:
        inn = None
        director_name = context.raw_company.director_name
        since_on_position = context.raw_company.director_since

        if since_on_position:
            since_on_position = context.raw_company.director_since.replace("г.", "года")
            since_on_position = since_on_position.replace("с ", "")
            since_on_position = convert_ru_date_to_date_obj(since_on_position)

        if context.raw_company.management_section and director_name:
            section = context.raw_company.management_section
            inn = extract_inn_by_director(section, director_name)

        if director_name:
            CEO = Manager(
                position=ManagerType.CEO,
                full_name=director_name,
                since_on_position=since_on_position,
                inn=inn
            )

            context.company_dto.management.append(CEO)
        next_step(context)
