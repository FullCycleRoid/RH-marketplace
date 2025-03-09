from pipelines.build_okveds.context import OkvedContext
from pipelines.generic_pipeline import Context, Pipeline, error_handler
from pipelines.utils import get_company_okved, get_random_company_okved

BATCH_SIZE = 10_000

def start_process():
    offset = 0
    times = 0
    company_count = 20_000_000
    company_count = 500_000

    unique_okveds = dict()

    # while times < 1000:
    #     okveds = get_random_company_okved(BATCH_SIZE)

    while offset < company_count:
        batch = get_company_okved(offset, BATCH_SIZE)
        for code_set in batch:
            if code_set[0]:
                for code, description in code_set[0].items():
                    if code not in unique_okveds:
                        unique_okveds[code] = description
                        print(len(unique_okveds))

    # legacy_ctx = OkvedContext()
    # load_legacy = Pipeline[Context](
    #
    # )
    # load_legacy(legacy_ctx, error_handler)


if __name__ == '__main__':
    start_process()
