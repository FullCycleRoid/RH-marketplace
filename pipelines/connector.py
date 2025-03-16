from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


async_postgres_uri = f'postgresql+psycopg2://cluster:cluster@localhost:15432/cluster_db'
psycopg_engine = create_engine(async_postgres_uri, echo=False, pool_size=200)
ClusterDBSession = sessionmaker(
    bind=psycopg_engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
)



async_postgres_uri = f'postgresql+psycopg2://admin:password123@localhost:25432/monolith'
psycopg_engine = create_engine(async_postgres_uri, echo=False, pool_size=200)
MarketplaceDBSession = sessionmaker(
    bind=psycopg_engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
)
