from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from src.config import cors_config, URLPathsConfig, URLNamesConfig
from src.user.app import app as user_app
from src.company.app import app as company_app


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.ALLOW_ORIGINS,
    allow_credentials=cors_config.ALLOW_CREDENTIALS,
    allow_methods=cors_config.ALLOW_METHODS,
    allow_headers=cors_config.ALLOW_HEADERS,
)


@app.get(
    path=URLPathsConfig.HOMEPAGE,
    response_class=RedirectResponse,
    name=URLNamesConfig.HOMEPAGE,
    status_code=status.HTTP_303_SEE_OTHER
)
async def homepage():
    return RedirectResponse(
        status_code=status.HTTP_303_SEE_OTHER,
        url=URLPathsConfig.DOCS
    )

app.mount("/api/user", user_app)
app.mount("/api/company", company_app)
