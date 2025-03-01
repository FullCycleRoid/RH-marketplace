from sqlalchemy.ext.asyncio import AsyncSession

from pipelines.company_loader.connector import get_cluster_db
from pipelines.company_loader.raw_model import RawCompany
from pipelines.generic_pipeline import Context, NextStep


class LoadCompanyStep:
    def __init__(self, connection: AsyncSession = get_cluster_db()) -> None:
        self._connection = connection

    def __call__(self, context: Context, next_step: NextStep) -> None:
        raw_company: RawCompany = self.get_raw_company()
        print(raw_company, 'raw_company raw_company')
        next_step(context)


    async def get_raw_company(self) -> RawCompany:
        return self._connection.execute(RawCompany).where(RawCompany.id == 1)

