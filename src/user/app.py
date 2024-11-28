from fastapi import FastAPI

from src.user.entrypoints.routers import router

app = FastAPI()

app.include_router(router, tags=["User"])
