from fastapi import FastAPI

from src.core.containers import AuthContainer

auth_app = FastAPI()
auth_app.container = AuthContainer()
