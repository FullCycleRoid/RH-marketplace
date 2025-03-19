from ml_models.paraphraser import paraphrase

from pipelines.generic_pipeline import Context, NextStep


class RewriteReliabilityAssessmentStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:

        assessments = []

        # TODO save load in file
        seen = {}

        for assessment in context.raw_company.reliability_assessment[2:-2].split('","'):
            if assessment not in seen:
                result = paraphrase(assessment)
                seen[assessment] = result
            else:
                result = seen[assessment]

            assessments.append(result)

        context.company_dto.reliability_assessment = assessments
        next_step(context)
