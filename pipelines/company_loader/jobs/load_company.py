
from pipelines.company_loader.contexts import CompanyContext
from pipelines.company_loader.steps.load_company_step import LoadRawCompanyStep
from pipelines.company_loader.utils import get_active_companies, get_active_company_count
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
    BATCH_SIZE = 100
    offset = 0

    count_companies = get_active_company_count()

    while count_companies < offset:
        batch_companies = get_active_companies(offset, BATCH_SIZE)

        # у меня BATCH_SIZE 100 компаний. Помоги мне запустить обработку каждой компании в отдельном пайплайне в отдельном треде
        # я хочу чтобы каждый пайпланй для обработки каждой компании обрабатывался в отдельном потоке.
        # Таким образом обрабаывается весь batch и потом загружается следующие 100 компаний и обрабатываются в отдельных потоках каждая.

        # Напиши мне так же пример где по такой же логике обработка каждой компании запускается в отдельном процессе мультипроцессинг

        # и сравни время обработки многопоточности, многопроцессности и прсото последовательной обработки

        company_ctx = CompanyContext()
        process_company = Pipeline[Context](
            LoadRawCompanyStep(),
            # AnotherStep1(),
            # AnotherStep2(),
            # AnotherStep3(),
        )
        process_company(company_ctx, error_handler)

        offset += offset



if __name__ == '__main__':
    start_process()
