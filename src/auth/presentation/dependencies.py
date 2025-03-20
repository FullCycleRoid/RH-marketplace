from src.auth.application.managers.auth_manager import AuthManager
from src.core.containers.auth_container import AuthContainer
from src.auth.main import user_app


from typing import Annotated

from fastapi import Depends

from src.auth.application.services.auth_servcies import AuthService
from src.auth.application.services.user_services import RedisUserService
from src.auth.infrastructure.repositories.postgres import \
    SQLAlchemyRefreshTokensRepository


def get_refresh_repo()
    return SQLAlchemyRefreshTokensRepository()

def get_auth_service(
    repo: SQLAlchemyRefreshTokensRepository = Depends(get_refresh_repo),
) -> AuthService:
    return AuthService(refresh_repository=repo)


def get_cache_service() -> RedisUserService:
    return RedisUserService()


def get_auth_manager(
    container: AuthContainer = Depends(lambda: user_app.container)
) -> AuthManager:
    return container.auth_manager()




CacheServiceDep = Annotated[RedisUserService, Depends(get_cache_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
AuthManagerDep = Annotated[AuthManager, Depends(get_auth_manager)]
