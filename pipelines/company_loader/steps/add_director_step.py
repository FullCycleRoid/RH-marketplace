from pipelines.utils import convert_ru_date_to_date_obj
from pipelines.generic_pipeline import Context, NextStep
from src.company.dto import Manager
from src.company.enums import ManagerType


class AddDirectorStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:
        director_name = context.raw_company.director_name
        if director_name:
            split_name = director_name.split(' ')
            if len(split_name) == 3:
                surname, name, patronymic = split_name

            if len(split_name) == 2:
                surname, name = split_name
                patronymic = None

            if len(split_name) == 4:
                surname, name, patronymic1, patronymic2  = split_name
                patronymic = patronymic1 + patronymic2

            since_on_position = context.raw_company.director_since.replace('г.', 'года')
            since_on_position = since_on_position.replace('с ', '')

            CEO = Manager(
                    position=ManagerType.CEO,
                    name=name,
                    patronymic=patronymic,
                    surname=surname,
                    since_on_position=convert_ru_date_to_date_obj(since_on_position)
                )

            context.company_dto.management.append(CEO)

        next_step(context)
