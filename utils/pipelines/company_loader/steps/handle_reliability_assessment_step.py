from utils.pipelines.generic_pipeline import Context, NextStep, PipelineStep


class HandleReliabilityAssessmentStep(PipelineStep):
    def __call__(self, context: Context, next_step: NextStep) -> None:
        ru_assessments = []

        r_assessment = context.raw_company.reliability_assessment
        if (
            context.raw_company.reliability_assessment
            and "Реквизиты,ОГРН,ИНН,КПП" not in r_assessment
        ):
            for assessment in r_assessment[2:-2].split('","'):
                ru_assessments.append(assessment)

            context.company_dto.advantages.extend(ru_assessments)

        next_step(context)
