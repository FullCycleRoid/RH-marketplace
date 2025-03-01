import asyncio

from loader_pipelines.generic_pipeline import Pipeline, Context, error_handler


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
    row_company_data_ctx = LegacyContext()
    load_legacy = Pipeline[Context](
        LoadLegacyStep()
    )
    load_legacy(legacy_ctx, error_handler)

    for user in legacy_ctx.users:
        row_ctx = RowContext(legacy=legacy_ctx, legacy_record=user)
        process_item = Pipeline[Context](
            # CheckUserExistStep(),
            # CreateNewUserStep(),
            # SetCorrectUserPhoneStep()
        )
        process_item(row_ctx, error_handler)
        print(f'Finish with failed: {row_ctx.failed_records}')


if __name__ == '__main__':
    start_process()
