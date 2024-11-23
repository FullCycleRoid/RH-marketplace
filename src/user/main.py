from fastapi import FastAPI

from src.config import app_configs
from src.user.routers import router

app = FastAPI(**app_configs)

app.include_router(router, tags=["User"])
