from pprint import pprint

from sqlalchemy.exc import DatabaseError

from pipelines.company_loader.okved_mapper import OkvedMapper
from pipelines.generic_pipeline import Context, NextStep, PipelineStep
from pipelines.utils import get_okved_by_code


class OkvedM2MIdsStep(PipelineStep):
    def __call__(self, context: Context, next_step: NextStep) -> None:
        okved_ids = []
        mapper = OkvedMapper("../okved.csv")

        for old_code, description in context.raw_company.okved.items():
            try:
                print("Lets try to find OKVED by old code")
                old_code_res = get_okved_by_code(old_code)
                if old_code_res and old_code_res.name == description:
                    print("********************")
                    print("Описание ОКВЕД и коды одинаковые")
                    print(old_code, description)
                    print(old_code_res.code, old_code_res.name)
                    print("********************")
                    okved_ids.append(old_code_res.id)
                else:
                    new_code = mapper.get_new_code(old_code)
                    if new_code:
                        new_code_res = get_okved_by_code(new_code)
                        if new_code_res:
                            print("**********************************")
                            print(
                                f"Okved not found by old code {old_code}. Lets try to get it by new code"
                            )
                            print(old_code, description)
                            print(new_code_res.code, new_code_res.name)
                            print("**********************************")
                            okved_ids.append(new_code_res.id)
            except DatabaseError:
                print("Database Error ........")
                continue

        context.company_dto.okved_ids = okved_ids
        pprint(context.company_dto.__dict__)
        next_step(context)
