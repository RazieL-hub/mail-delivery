from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import get_settings

DATABASE_URL = get_settings().database_sync_url


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    engine,
    autocommit=False,
    expire_on_commit=False,
)


def get_session() -> SessionLocal:
    with SessionLocal() as session:
        yield session