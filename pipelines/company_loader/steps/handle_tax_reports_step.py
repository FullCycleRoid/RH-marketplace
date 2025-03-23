from pipelines.company_loader.dto import TaxReport
from pipelines.generic_pipeline import Context, NextStep
from pipelines.utils import convert_to_numeric


class HandleTaxReportStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:
        taxes_paid = context.raw_company.taxes_paid
        paid_insurance = context.raw_company.paid_insurance
        if taxes_paid:
            taxes_paid = taxes_paid.replace("Уплачены налоги на сумму ", "")
            taxes_paid = convert_to_numeric(taxes_paid)

        if paid_insurance:
            paid_insurance = paid_insurance.replace(
                "Уплачены страховые взносы на сумму ", ""
            )
            paid_insurance = convert_to_numeric(paid_insurance)

        context.company_dto.tax_reports.append(
            TaxReport(year="2023", taxes_paid=taxes_paid, paid_insurance=paid_insurance)
        )
        next_step(context)
