from fastapi import FastAPI

from src.core.containers import ProductContainer

product_app = FastAPI()
product_app.container = ProductContainer()
