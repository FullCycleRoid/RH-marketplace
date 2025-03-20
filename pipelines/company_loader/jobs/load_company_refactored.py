import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from pipelines.company_loader.context import CompanyContext
from pipelines.company_loader.steps.add_director_step import AddDirectorStep
from pipelines.company_loader.steps.convert_registration_date import \
    ConvertRegistrationDateStep
from pipelines.company_loader.steps.create_dto_step import CreateCompanyDTOStep
from pipelines.company_loader.steps.handle_advantages_step import \
    HandleAdvantagesStep
from pipelines.company_loader.steps.handle_authorized_capital import \
    ConvertAuthorizedCapitalStep
from pipelines.company_loader.steps.handle_average_number_of_employees import \
    ConvertAverageNumberOfEmployeesStep
from pipelines.company_loader.steps.handle_contacts_step import \
    HandleContactsStep
from pipelines.company_loader.steps.handle_financial_reports_step import \
    HandleFinancialReportStep
from pipelines.company_loader.steps.handle_reliability_assessment_step import \
    HandleReliabilityAssessmentStep
from pipelines.company_loader.steps.handle_tax_reports_step import \
    HandleTaxReportStep
from pipelines.company_loader.steps.match_legal_status_step import \
    MatchLegalStateStep
from pipelines.company_loader.steps.okved_step import OkvedM2MIdsStep
from pipelines.generic_pipeline import Context, Pipeline, error_handler
from pipelines.utils import get_active_companies


BATCH_SIZE = 100
MAX_COMPANIES = 20_000_000


def process_single_company(company, process_pipeline, error_handler):
    """Обработка одной компании"""
    company_ctx = CompanyContext()
    company_ctx.raw_company = company
    process_pipeline(company_ctx, error_handler)

def process_batch_sequential(batch, process_pipeline, error_handler):
    """Последовательная обработка батча"""
    for company in batch:
        process_single_company(company, process_pipeline, error_handler)

def process_batch_threaded(batch, process_pipeline, error_handler):
    """Многопоточная обработка батча"""
    with ThreadPoolExecutor(max_workers=BATCH_SIZE) as executor:
        futures = [
            executor.submit(
                process_single_company,
                company,
                process_pipeline,
                error_handler
            ) for company in batch
        ]
        for future in futures:
            future.result()  # Ожидаем завершения всех задач

def process_batch_multiprocess(batch, process_pipeline, error_handler):
    """Многопроцессная обработка батча"""
    ctx = multiprocessing.get_context("spawn")

    with ProcessPoolExecutor(mp_context=ctx) as executor:
        futures = [
            executor.submit(
                process_single_company,
                company,
                process_pipeline,
                error_handler
            ) for company in batch
        ]
        for future in futures:
            future.result()

def start_process(translator = None):
    offset = 0

    process_pipeline = Pipeline[Context](
        CreateCompanyDTOStep(translator),
        ConvertRegistrationDateStep(),
        MatchLegalStateStep(),
        ConvertAuthorizedCapitalStep(),
        ConvertAverageNumberOfEmployeesStep(),
        HandleContactsStep(),
        AddDirectorStep(translator),
        HandleFinancialReportStep(),
        HandleTaxReportStep(),
        HandleReliabilityAssessmentStep(translator),
        HandleAdvantagesStep(translator),
        OkvedM2MIdsStep(),
        BuildCompanyDBModel(),
    )

    while offset < MAX_COMPANIES:
        batch = get_active_companies(offset, BATCH_SIZE)
        if not batch:
            break

        start = time.perf_counter()
        process_batch_multiprocess(batch, process_pipeline, error_handler)
        process_time = time.perf_counter() - start

        offset += BATCH_SIZE
        print(f"Обрабатано {offset} компаний. ")
        print(f"{BATCH_SIZE} компаний обработано за {process_time:.2f} сек")

if __name__ == '__main__':
    start_process()