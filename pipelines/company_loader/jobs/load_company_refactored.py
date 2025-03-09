import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from pipelines.company_loader.context import CompanyContext
from pipelines.company_loader.steps.handle_advantages_step import HandleAdvantagesStep
from pipelines.company_loader.steps.handle_reliability_assessment_step import HandleReliabilityAssessmentStep
from pipelines.company_loader.steps.convert_registration_date import ConvertRegistrationDateStep
from pipelines.company_loader.steps.create_dto_step import CreateCompanyDTOStep
from pipelines.company_loader.steps.handle_authorized_capital import ConvertAuthorizedCapitalStep
from pipelines.company_loader.steps.handle_average_number_of_employees import ConvertAverageNumberOfEmployeesStep
from pipelines.company_loader.steps.handle_contacts_step import HandleContactsStep
from pipelines.company_loader.steps.add_director_step import AddDirectorStep
from pipelines.company_loader.steps.handle_financial_reports_step import HandleFinancialReportStep
from pipelines.company_loader.steps.handle_tax_reports_step import HandleTaxReportStep
from pipelines.company_loader.steps.match_legal_status_step import MatchLegalStateStep
from pipelines.utils import get_active_companies
from pipelines.generic_pipeline import Pipeline, Context, error_handler

BATCH_SIZE = 30


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
    with ProcessPoolExecutor() as executor:
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

def benchmark_processing():
    """Сравнение времени разных методов обработки"""
    test_batch = get_active_companies(0, BATCH_SIZE)
    process_pipeline = Pipeline[Context](
        CreateCompanyDTOStep(),
        ConvertRegistrationDateStep(),
        MatchLegalStateStep(),
        ConvertAuthorizedCapitalStep(),
        ConvertAverageNumberOfEmployeesStep(),
        HandleContactsStep(),
        AddDirectorStep(),
        HandleFinancialReportStep(),
        HandleTaxReportStep(),
        # RewriteReliabilityAssessmentStep(),
        HandleReliabilityAssessmentStep(),
        HandleAdvantagesStep(),
    )

    # Тестируем последовательную обработку
    start = time.perf_counter()
    process_batch_sequential(test_batch, process_pipeline, error_handler)
    seq_time = time.perf_counter() - start

    # Тестируем многопоточную обработку
    start = time.perf_counter()
    process_batch_threaded(test_batch, process_pipeline, error_handler)
    thread_time = time.perf_counter() - start

    # Тестируем многопроцессную обработку
    start = time.perf_counter()
    process_batch_multiprocess(test_batch, process_pipeline, error_handler)
    process_time = time.perf_counter() - start

    print(f"\nРезультаты сравнения (батч {BATCH_SIZE} компаний):")
    print(f"Последовательная обработка: {seq_time:.2f} сек")
    print(f"Многопоточная обработка:   {thread_time:.2f} сек")
    print(f"Многопроцессная обработка: {process_time:.2f} сек")

# def start_process():
#     count_companies = get_active_company_count()
#     offset = 0
#
#     process_pipeline = Pipeline[Context](
#         LoadRawCompanyStep()
#     )
#     error_handler = ...  # Ваш обработчик ошибок
#
#     while offset < count_companies:  # Исправлено условие
#         batch = get_active_companies(offset, BATCH_SIZE)
#         if not batch:
#             break
#
#         # Выберите нужный метод обработки:
#         # process_batch_sequential(batch, process_pipeline, error_handler)
#         # process_batch_threaded(batch, process_pipeline, error_handler)
#         # process_batch_multiprocess(batch, process_pipeline, error_handler)
#
#         offset += BATCH_SIZE  # Исправлено увеличение offset

if __name__ == '__main__':
    # Для корректной работы multiprocessing в Windows
    benchmark_processing()  # Запуск сравнения производительности
    # start_process()  # Основной пайплайн