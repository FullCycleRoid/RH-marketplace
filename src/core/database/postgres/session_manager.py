from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

class DatabaseSessionManager:
    _engine = None
    _sessionmaker = None

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            async_postgres_uri = (
                "postgresql+psycopg2://admin:password123@localhost:25432/monolith"
            )
            cls._engine = create_engine(
                async_postgres_uri,
                echo=False,
                pool_size=1000
            )
        return cls._engine

    @classmethod
    def get_sessionmaker(cls):
        if cls._sessionmaker is None:
            engine = cls.get_engine()
            cls._sessionmaker = sessionmaker(
                bind=engine,
                autoflush=False,
                expire_on_commit=False,
                autocommit=False
            )
        return cls._sessionmaker
