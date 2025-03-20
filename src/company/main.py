from fastapi import FastAPI

from src.core.containers import CompanyContainer

company_app = FastAPI()
company_app.container = CompanyContainer()
