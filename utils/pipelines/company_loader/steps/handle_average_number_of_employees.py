from utils.pipelines.generic_pipeline import Context, NextStep, PipelineStep


class ConvertAverageNumberOfEmployeesStep(PipelineStep):
    def __call__(self, context: Context, next_step: NextStep) -> None:
        raw_data = context.raw_company.average_number_of_employees
        if raw_data:
            employees = "".join(char for char in raw_data if char.isdigit())
            if employees:
                context.company_dto.average_number_of_employees = int(employees)
        next_step(context)
