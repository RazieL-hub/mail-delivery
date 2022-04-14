from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import get_settings

DATABASE_URL = get_settings().database_async_url

Base = declarative_base()

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)

Session = sessionmaker(
    bind=engine,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_session() -> Session:
    async with Session() as session:
        yield session
