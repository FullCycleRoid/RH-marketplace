from typing import Any, Dict, List

from click.testing import Result
from fastapi import HTTPException
from sqlalchemy import CursorResult, Delete, Engine, Insert, Select, Update
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.orm import scoped_session, sessionmaker

from src.core.database.postgres.connectors import PsycopgAsyncSessionFactory, PsycopgSyncSessionFactory, psycopg_engine, psycopg_sync_engine
from src.core.logger import logger


def get_sync_session(sync_session_factory: sessionmaker = PsycopgSyncSessionFactory):
    return scoped_session(sync_session_factory)


def sync_fetch_one(query: Select | Insert | Update, sync_engine: Engine = psycopg_sync_engine) -> Dict[str, Any] | None:
    with sync_engine.begin() as conn:
        try:
            cursor: CursorResult = conn.execute(query)
            return cursor.first()._asdict() if cursor.rowcount > 0 else None

        except OperationalError as e:
            logger.warn(e)
            raise HTTPException(500, e)


async def fetch_one(query: Select | Insert | Update, engine: AsyncEngine = psycopg_engine) -> Dict[str, Any] | None:
    async with engine.begin() as conn:
        try:
            cursor: CursorResult = await conn.execute(query)
            return cursor.first()._asdict() if cursor.rowcount > 0 else None

        except OperationalError as e:
            logger.warn(e)
            raise HTTPException(500, e)


async def fetch_all(query: Select | Insert | Update, engine: AsyncEngine = psycopg_engine) -> List[Dict[str, Any]]:
    async with engine.begin() as conn:
        try:
            cursor: CursorResult = await conn.execute(query)
            return [r._asdict() for r in cursor.all()]

        except OperationalError as e:
            logger.warn(e)
            raise HTTPException(500, e)


async def execute(query: Select | Insert | Update | Delete, engine: AsyncEngine = psycopg_engine) -> Any | None:
    async with engine.begin() as conn:
        try:
            return await conn.execute(query)

        except OperationalError as e:
            logger.warn(e)
            raise HTTPException(500, e)


async def session_fetch_one(
    query: Select | Insert | Update, session_factory: async_sessionmaker = PsycopgAsyncSessionFactory
) -> Dict[str, Any] | None:
    async with session_factory() as sess:
        try:
            result: Result = await sess.execute(query)
            if not isinstance(query, Select):
                await sess.commit()

            res = result.scalar()
            return res.__dict__ if res else None

        except OperationalError as e:
            logger.warn(e)
            raise HTTPException(500, e)


async def session_fetch_all(query: Select | Insert | Update, session_factory: async_sessionmaker = PsycopgAsyncSessionFactory) -> List[Any]:
    async with session_factory() as sess:
        try:
            result: Result = await sess.execute(query)
            res = result.scalars().unique().all()
            if res:
                return [item.__dict__ for item in res]
            return []

        except OperationalError as e:
            logger.warn(e)
            raise HTTPException(500, e)


async def session_execute(query: Select | Insert | Update | Delete, session_factory: async_sessionmaker = PsycopgAsyncSessionFactory) -> Any | None:
    async with session_factory() as sess:
        try:
            return await sess.execute(query)

        except OperationalError as e:
            logger.warn(e)
            raise HTTPException(500, e)


async def execute_bulk(query: Insert | Update | Delete, param_list: List[Dict], engine: AsyncEngine = psycopg_engine) -> None:
    async with engine.begin() as conn:
        await conn.execute(query, param_list)
