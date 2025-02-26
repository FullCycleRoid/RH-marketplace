import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.company.router import router as company_router
from src.chat.router import router as chat_router
from src.products.router import router as products_router
from src.config import app_configs, settings


app = FastAPI(**app_configs)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router, prefix="/api/users", tags=["Auth"])
app.include_router(company_router, prefix="/api/company", tags=["Company"])
app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])
app.include_router(products_router, prefix="/api/products", tags=["Products"])


if settings.ENVIRONMENT.is_local:
    uvicorn.run(app=app)
