from pipelines.generic_pipeline import Context, NextStep
from src.core.language_translator.proxy_google_translator2 import translate, proxy_settings


class HandleReliabilityAssessmentStep:
    def __init__(self, translator = None):
        self.translator = translator

    def __call__(self, context: Context, next_step: NextStep) -> None:
        ru_assessments = []
        en_assessments = []

        r_assessment = context.raw_company.reliability_assessment
        if context.raw_company.reliability_assessment and "Реквизиты,ОГРН,ИНН,КПП" not in r_assessment:
            for assessment in r_assessment[2:-2].split('","'):
                ru_assessments.append(assessment)

                if assessment in context.translated_advantages:
                    en_assessment = context.translated_advantages[assessment]
                else:
                    en_assessment = translate(assessment, proxies=proxy_settings)
                    context.translated_advantages[assessment] = en_assessment

                en_assessments.append(en_assessment)

            context.company_dto.advantages.extend(ru_assessments)
            context.company_dto.en_advantages.extend(en_assessments)

            print("***********   ReliabilityAssessment   ***********")
            print(context.company_dto.advantages)
            print(context.company_dto.en_advantages,)
            print("**********************")
        next_step(context)
