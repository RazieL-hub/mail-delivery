import sqlalchemy

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.async_connect_postgres import Base

metadata = sqlalchemy.MetaData()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, nullable=True)
    telegram = Column(String(256), unique=True, nullable=True)
    viber = Column(String(256), unique=True, nullable=True)
    whats_app = Column(String(256), unique=True, nullable=True)

    config = relationship('EventConfig', back_populates='user')

    user_reports = relationship('Report', back_populates='users')

    class Config:
        orm_mode = True
