from utils.pipelines.company_loader.dto import FinancialReport
from utils.pipelines.generic_pipeline import Context, NextStep, PipelineStep
from utils.pipelines.utils import convert_to_numeric


class HandleFinancialReportStep(PipelineStep):
    def __call__(self, context: Context, next_step: NextStep) -> None:
        annual_income = convert_to_numeric(context.raw_company.annual_income)
        net_profit = convert_to_numeric(context.raw_company.net_profit)
        context.company_dto.financial_reports.append(
            FinancialReport(
                year="2023",
                annual_income=annual_income,
                net_profit=net_profit,
                currency="RUB",
            )
        )

        next_step(context)
