from pipelines.generic_pipeline import Context, NextStep
from src.core.language_translator.google_translator import translate_large_text
from src.core.language_translator.ml_traslator import LangTranslator


class HandleReliabilityAssessmentStep:
    def __init__(self, translator: LangTranslator):
        self.translator = translator

    def __call__(self, context: Context, next_step: NextStep) -> None:
        ru_assessments = []
        en_assessments = []

        r_assessment = context.raw_company.reliability_assessment
        if "Реквизиты,ОГРН,ИНН,КПП" not in r_assessment:
            if context.raw_company.reliability_assessment:
                for assessment in r_assessment[2:-2].split('","'):
                    ru_assessments.append(assessment)
                    en_assessments.append(self.translator(assessment))

                context.company_dto.advantages.extend(ru_assessments)
                context.company_dto.en_advantages.extend(en_assessments)
            print("***********   ReliabilityAssessment   ***********")
            print(context.company_dto.advantages)
            print(context.company_dto.en_advantages,)
            print("**********************")
        next_step(context)
