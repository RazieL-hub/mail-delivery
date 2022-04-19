import sqlalchemy

from sqlalchemy import Column, Integer, String
from database.async_connect_postgres import Base

metadata = sqlalchemy.MetaData()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, nullable=True)
    telegram = Column(String(256), unique=True, nullable=True)
    viber = Column(String(256), unique=True, nullable=True)
    whats_app = Column(String(256), unique=True, nullable=True)

    class Config:
        orm_mode = True