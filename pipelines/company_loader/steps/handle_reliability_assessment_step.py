from pipelines.generic_pipeline import Context, NextStep


class HandleReliabilityAssessmentStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:
        rewrite_assessment = []

        for assessment in context.raw_company.reliability_assessment[2:-2].split('","'):
            rewrite_assessment.append(assessment)

        context.company_dto.reliability_assessment = rewrite_assessment

        next_step(context)
