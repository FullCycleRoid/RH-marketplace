import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth.main import app as auth_app
from src.catalog.main import app as catalog_app
from src.catalog.main import app as company_app
from src.chat.main import app as chat_app
from src.core.config.config import app_configs, settings
from src.core.containers.base_container import BaseContainer
from src.products.main import product_app

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


app.mount("/api/user", auth_app)
app.mount("/api/company", company_app)
app.mount("/api/catalog", catalog_app)
app.mount("/api/chat", chat_app)
app.mount("/api/products", product_app)

if settings.ENVIRONMENT.is_local:
    uvicorn.run(app=app)
