import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.catalog.main import app as catalog_app
from src.catalog.main import app as company_app
from src.chat.main import app as chat_app
from src.config import app_configs, settings
from src.products.main import app as products_app
from src.user.main import app as user_app

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


app.mount(path="/api/user", app=user_app, name="User app")
app.mount(path="/api/company", app=company_app, name="Company app")
app.mount(path="/api/catalog", app=catalog_app, name="Catalog app")
app.mount(path="/api/chat", app=chat_app, name="Chat app")
app.mount(path="/api/products", app=products_app, name="Products app")


if settings.ENVIRONMENT.is_local:
    uvicorn.run(app=app)
