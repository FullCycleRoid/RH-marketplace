from pipelines.company_loader.contexts import CompanyContext
from pipelines.company_loader.steps.load_company_step import LoadRawCompanyStep
from pipelines.generic_pipeline import Context, Pipeline, error_handler


async def ru_company_loader():
    # load raw data

    # extract legal data
    # extract tax reports
    # extract financial reports

    # handle registration_date
    # handle legal_form
    # handle authorized_capital
    # handle average_number_of_employees

    # build company_loader DTO
    # build address DTO
    # build contacts DTO
    # build management DTO
    # build financial_reports DTO
    # build tax_reports DTO

    # match OKVEDs

    # build translations
    pass

def start_process():
    company_ctx = CompanyContext()

    while company_ctx.current_id < 10000:
        load_legacy = Pipeline[Context](
            LoadRawCompanyStep()
        )
        load_legacy(company_ctx, error_handler)

        company_ctx.current_id += 1


if __name__ == '__main__':
    start_process()
