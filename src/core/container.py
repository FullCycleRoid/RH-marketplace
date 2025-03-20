import redis.asyncio as Redis
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config.config import create_config_adapter, settings


class BaseContainer(containers.DeclarativeContainer):
    config = create_config_adapter(settings)

    # Асинхронный движок PostgreSQL
    async_engine = providers.Singleton(
        create_async_engine,
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
        echo=settings.DB_ECHO,
        pool_size=settings.POOL_SIZE,
    )

    # Фабрика асинхронных сессий SQLAlchemy
    async_session_factory = providers.Singleton(
        sessionmaker,
        bind=async_engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
        autocommit=False,
    )

    # Redis пул соединений
    redis_pool = providers.Singleton(
        Redis.ConnectionPool.from_url,
        f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        max_connections=settings.MAX_POOL_CONNECTIONS,
        decode_responses=True,
    )

    # Redis клиент
    redis_client = providers.Singleton(
        Redis,
        connection_pool=redis_pool,
    )
