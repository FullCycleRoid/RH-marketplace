from fastapi import FastAPI

from src.core.containers import CatalogContainer

catalog_app = FastAPI()
catalog_app.container = CatalogContainer()
