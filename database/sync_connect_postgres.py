from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql://postgres:postgres@postgres:5432/postgres",
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