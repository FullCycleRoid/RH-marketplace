# To cluster DB parsing module connector
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings


async_postgres_uri = f'postgresql+asyncpg://cluster:cluster@localhost:15432/cluster_db'
psycopg_engine = create_async_engine(async_postgres_uri, echo=settings.DB_ECHO, pool_size=200)
SessionFactory = async_sessionmaker(
    bind=psycopg_engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
)


def get_cluster_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
