import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Dict, List

from pipelines.company_loader.context import CompanyContext
from pipelines.company_loader.steps.add_director_step import AddDirectorStep
from pipelines.company_loader.steps.build_company_db_model import BuildCompanyDBModel
from pipelines.company_loader.steps.convert_registration_date import (
    ConvertRegistrationDateStep,
)
from pipelines.company_loader.steps.create_dto_step import CreateCompanyDTOStep
from pipelines.company_loader.steps.handle_advantages_step import HandleAdvantagesStep
from pipelines.company_loader.steps.handle_authorized_capital import (
    ConvertAuthorizedCapitalStep,
)
from pipelines.company_loader.steps.handle_average_number_of_employees import (
    ConvertAverageNumberOfEmployeesStep,
)
from pipelines.company_loader.steps.handle_contacts_step import HandleContactsStep
from pipelines.company_loader.steps.handle_financial_reports_step import (
    HandleFinancialReportStep,
)
from pipelines.company_loader.steps.handle_reliability_assessment_step import (
    HandleReliabilityAssessmentStep,
)
from pipelines.company_loader.steps.handle_tax_reports_step import HandleTaxReportStep
from pipelines.company_loader.steps.match_legal_status_step import MatchLegalStateStep
from pipelines.company_loader.steps.okved_step import OkvedM2MIdsStep
from pipelines.generic_pipeline import Context, Pipeline, error_handler
from pipelines.utils import get_active_companies, get_all_field_types
from src import CompanyFieldType

BATCH_SIZE = 100
MAX_COMPANIES = 20_000_000


def process_single_company(
    company, field_type_ids, proxies, process_pipeline, error_handler
):
    """Обработка одной компании"""
    company_ctx = CompanyContext(
        field_type_ids=field_type_ids, proxies=proxies, raw_company=company
    )
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
                process_single_company, company, process_pipeline, error_handler
            )
            for company in batch
        ]
        for future in futures:
            future.result()  # Ожидаем завершения всех задач


def process_batch_multiprocess(
    batch, field_type_ids, proxies, process_pipeline, error_handler
):
    """Многопроцессная обработка батча"""
    ctx = multiprocessing.get_context("spawn")

    with ProcessPoolExecutor(mp_context=ctx) as executor:
        futures = [
            executor.submit(
                process_single_company,
                company,
                field_type_ids,
                proxies,
                process_pipeline,
                error_handler,
            )
            for company in batch
        ]
        for future in futures:
            future.result()


def match_field_type_names() -> Dict:
    field_match = dict()
    field_names = [
        "name",
        "legal_name",
        "inn",
        "registration_date",
        "liquidation_date",
        "legal_address",
        "ogrn",
        "kpp",
        "okpo",
        "authorized_capital",
        "average_number_of_employees",
        "advantages",
        "okogu_code",
        "okopf_code",
        "okfs_code",
        "okato_code",
        "oktmo_code",
        "kladr_code",
    ]
    field_types: List[CompanyFieldType] = get_all_field_types()

    for name in field_names:
        for type in field_types:
            if name == type.en_name:
                field_match[name] = type.id

    return field_match


def load_proxies(file_path: str) -> List[str]:
    with open(file_path, "r") as f:
        lines = f.readlines()
        return [f"https://{proxy.strip()}" for proxy in lines]


def start_process(translator=None):
    start_process_time = time.perf_counter()
    offset = 0

    field_type_ids = match_field_type_names()
    PROXIES = load_proxies("../../../proxylist.txt")

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

        start_batch_time = time.perf_counter()
        process_batch_multiprocess(
            batch, field_type_ids, PROXIES, process_pipeline, error_handler
        )
        process_batch_time = time.perf_counter() - start_batch_time
        process_time = time.perf_counter() - start_process_time

        offset += BATCH_SIZE
        print(f"Обрабатано {offset} компаний. ")
        print(f"{BATCH_SIZE} компаний обработано за {process_batch_time:.2f} сек")
        print(f"Всего {offset} компаний обработано за {process_time:.2f} сек")


if __name__ == "__main__":
    start_process()
