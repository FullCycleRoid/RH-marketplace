from requests import Session

from pipelines.company_loader.connector import SessionFactory
from pipelines.company_loader.raw_model import RawCompany
from pipelines.generic_pipeline import Context, NextStep


class LoadRawCompanyStep:
    def __init__(self, session: Session = SessionFactory) -> None:
        self._session = session

    def __call__(self, context: Context, next_step: NextStep) -> None:
        raw_company: RawCompany = self.get_raw_company(context)
        print(raw_company.id, raw_company.inn)
        context.raw_company = raw_company
        next_step(context)


    def get_raw_company(self, context) -> RawCompany:
        with self._session() as session:
            res = session.query(RawCompany).where(RawCompany.id == context.current_id)
            return res.first()
