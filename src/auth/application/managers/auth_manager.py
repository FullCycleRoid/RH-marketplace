from src.auth.application.di import AuthServiceDep, CacheServiceDep
from src.auth.infrastructure.models import User


class AuthManager:
    def __init__(self, auth_service: AuthServiceDep, cache_service: CacheServiceDep):
        self.auth_service = auth_service
        self.cache_service = cache_service

    async def authenticate_user(self, jwt_data: JWTData) -> User:
        user = await self.auth_service.get_user_by_id(jwt_data.user_id)
        # Логика авторизации...
        return user

    async def get_current_user(self, jwt_data: JWTData) -> User:
        # Логика получения пользователя...
        return user
