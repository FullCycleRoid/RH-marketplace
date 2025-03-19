from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import app_configs

app = FastAPI(**app_configs)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
