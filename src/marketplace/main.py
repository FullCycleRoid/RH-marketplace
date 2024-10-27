from fastapi import FastAPI

from src.config import app_configs
from src.marketplace.user.router import router as user_router

app = FastAPI(**app_configs)

app.include_router(user_router, prefix="/user", tags=["User"])
# app.include_router(companies_router, prefix="/companies", tags=["Companies"])
