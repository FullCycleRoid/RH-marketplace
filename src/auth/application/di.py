from typing import Annotated

from fastapi import Depends

from src.auth.application.services.auth_servcies import AuthService
from src.auth.application.services.user_services import RedisUserService
from src.auth.infrastructure.repositories.postgres import \
    SQLAlchemyRefreshTokensRepository


def get_auth_service(
    repo: SQLAlchemyRefreshTokensRepository = Depends(get_refresh_repo),
) -> AuthService:
    return AuthService(refresh_repository=repo)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_cache_service() -> RedisUserService:
    return RedisUserService()


CacheServiceDep = Annotated[RedisUserService, Depends(get_cache_service)]
