import redis.asyncio as Redis
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.cache.redis.repositories import RedisRepository
from src.core.config.adapter import create_config_adapter
from src.core.config.config import settings


class BaseContainer(containers.DeclarativeContainer):
    config = create_config_adapter(settings)

    # Асинхронный движок PostgreSQL
    async_engine = providers.Singleton(
        create_async_engine,
        f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}",
        echo=config.DB_ECHO,
        pool_size=config.POOL_SIZE,
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

    async_session = providers.Resource(async_session_factory)

    # Redis пул соединений
    redis_pool = providers.Singleton(
        Redis.ConnectionPool.from_url,
        f"redis://:{config.REDIS_PASSWORD}@{config.REDIS_HOST}:{config.REDIS_PORT}",
        max_connections=config.MAX_POOL_CONNECTIONS,
        decode_responses=True,
    )

    # Redis клиент
    redis_client = providers.Singleton(
        Redis,
        connection_pool=redis_pool,
    )

    redis_repo = providers.Singleton(RedisRepository, client=redis_client)
