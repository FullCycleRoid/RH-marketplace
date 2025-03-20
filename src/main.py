import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth.main import app as user_app
from src.catalog.main import app as catalog_app
from src.catalog.main import app as company_app
from src.chat.main import app as chat_app
from src.core.config.config import app_configs, settings
from src.core.container import BaseContainer
from src.products.main import app as products_app

app = FastAPI(**app_configs)
app.container = BaseContainer()


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


def mount_subapp(main_app: FastAPI, path: str, subapp: FastAPI):
    # Передача контейнера в подприложение
    if hasattr(main_app, "container"):
        subapp.container.parent = main_app.container
    main_app.mount(path, subapp)


mount_subapp(app, "/api/user", user_app)
mount_subapp(app, "/api/company", company_app)
mount_subapp(app, "/api/catalog", catalog_app)
mount_subapp(app, "/api/chat", chat_app)
mount_subapp(app, "/api/products", products_app)


if settings.ENVIRONMENT.is_local:
    uvicorn.run(app=app)
