import sqlalchemy

from sqlalchemy import Column, Integer, String, TIME, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from database.async_connect_postgres import Base

metadata = sqlalchemy.MetaData()


class EventConfig(Base):
    __tablename__ = 'events_config'
    id = Column(Integer, primary_key=True, index=True)
    type_event = Column(String(256), )
    instant_delivery = Column(Boolean, default=False)
    periodic_time = Column(Integer, default=15)
    work_time_start = Column(TIME, )
    work_time_finish = Column(TIME, )
    last_send = Column(DateTime, server_default=now(), server_onupdate=now())
    user_id = Column(Integer, ForeignKey('users.user_id'))

    user = relationship('User', back_populates='config')
    event_settings = relationship('EventConfig', back_populates='event_id')

    class Config:
        orm_mode = True
