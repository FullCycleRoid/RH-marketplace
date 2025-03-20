from dependency_injector import containers, providers

from src.auth.application.managers.auth_manager import AuthManager
from src.auth.application.services.auth_servcies import AuthService
from src.auth.application.services.user_services import RedisUserService
from src.auth.infrastructure.repositories.postgres import \
    SQLAlchemyRefreshTokensRepository


class AuthContainer(containers.DeclarativeContainer):
    parent = providers.DependenciesContainer()

    # Repositories
    refresh_repo = providers.Factory(
        SQLAlchemyRefreshTokensRepository, session=parent.async_session_factory
    )

    # Services
    auth_service = providers.Factory(AuthService, refresh_repository=refresh_repo)

    redis_user_service = providers.Factory(
        RedisUserService, redis_client=parent.redis_client
    )

    # Managers
    auth_manager = providers.Factory(
        AuthManager, auth_service=auth_service, redis_service=redis_user_service
    )
