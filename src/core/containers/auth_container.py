from dependency_injector import containers, providers
from redis.asyncio import Redis

from src.auth.application.managers.auth_manager import AuthManager
from src.auth.application.services.auth_servcies import AuthService
from src.auth.application.services.user_services import RedisUserService, UserService
from src.auth.infrastructure.repositories.postgres import (
    SQLAlchemyRefreshTokensRepository,
    SQLAlchemyUsersRepository,
)
from src.core.cache.redis.repositories import RedisRepository


class AuthContainer(containers.DeclarativeContainer):
    parent = providers.DependenciesContainer()

    # Сессия БД
    async_session = providers.Resource(parent.async_session_factory)

    # Репозитории
    user_repo = providers.Factory(SQLAlchemyUsersRepository, session=async_session)

    refresh_repo = providers.Factory(
        SQLAlchemyRefreshTokensRepository, session=async_session
    )

    # Redis репозиторий
    redis_repo = providers.Singleton(
        RedisRepository, client=providers.Dependency(instance_of=Redis)
    )

    # Сервисы
    user_service = providers.Factory(UserService, user_repository=user_repo)

    auth_service = providers.Factory(AuthService, refresh_repository=refresh_repo)

    redis_user_service = providers.Factory(RedisUserService, cache=redis_repo)

    # Менеджеры
    auth_manager = providers.Factory(
        AuthManager,
        auth_service=auth_service,
        user_service=user_service,
        redis_service=redis_user_service,
    )
