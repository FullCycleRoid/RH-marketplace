from typing import Any

from click.testing import Result
from pydantic import PostgresDsn
from sqlalchemy import (
    CursorResult,
    Delete,
    Insert,
    Select,
    Update
)
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.config import settings


async_postgres_uri: PostgresDsn = f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'
psycopg_engine = create_async_engine(async_postgres_uri, echo=settings.DB_ECHO, poolclass=NullPool)
PsycopgAsyncSessionFactory = async_sessionmaker(
    bind=psycopg_engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
)

sync_postgres_uri: PostgresDsn = f'postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'
psycopg_sync_engine = create_engine(sync_postgres_uri, echo=settings.DB_ECHO)
SyncSessionMaker = sessionmaker(
    bind=psycopg_sync_engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
)


async def get_async_session() -> AsyncSession:
    async with PsycopgAsyncSessionFactory() as session:
        yield session


async def fetch_one(query: Select | Insert | Update) -> dict[str, Any] | None:
    async with psycopg_engine.begin() as conn:
        cursor: CursorResult = await conn.execute(query)
        return cursor.first()._asdict() if cursor.rowcount > 0 else None


async def fetch_all(query: Select | Insert | Update) -> list[dict[str, Any]]:
    async with psycopg_engine.begin() as conn:
        cursor: CursorResult = await conn.execute(query)
        return [r._asdict() for r in cursor.all()]


async def execute(query: Select | Insert | Update | Delete) -> Any | None:
    async with psycopg_engine.begin() as conn:
        return await conn.execute(query)


async def session_fetch_one(query: Select | Insert | Update) -> Any | None:
    async with PsycopgAsyncSessionFactory() as sess:
        result: Result = await sess.execute(query)
        if not isinstance(query, Select):
            await sess.commit()
        return result.scalar()


async def session_fetch_all(query: Select | Insert | Update) -> list[Any]:
    async with PsycopgAsyncSessionFactory() as sess:
        result: Result = await sess.execute(query)
        return result.scalars().unique().all()


async def session_execute(query: Select | Insert | Update | Delete) -> Any | None:
    async with PsycopgAsyncSessionFactory() as sess:
        return await sess.execute(query)


async def execute_bulk(query: Insert | Update | Delete, param_list: list[dict]) -> None:
    async with psycopg_engine.begin() as conn:
        await conn.execute(query, param_list)
