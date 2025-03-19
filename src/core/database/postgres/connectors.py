from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

async_postgres_uri = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
psycopg_engine = create_async_engine(
    async_postgres_uri, echo=settings.DB_ECHO, pool_size=200
)
PsycopgAsyncSessionFactory = async_sessionmaker(
    bind=psycopg_engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
)

sync_postgres_uri = f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
psycopg_sync_engine = create_engine(
    sync_postgres_uri, echo=settings.DB_ECHO, pool_size=200
)
PsycopgSyncSessionFactory = sessionmaker(
    bind=psycopg_sync_engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
)


def get_db():
    db = PsycopgAsyncSessionFactory()
    try:
        yield db
    finally:
        db.close()
