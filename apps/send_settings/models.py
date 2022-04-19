import sqlalchemy

from sqlalchemy import Column, Integer, String, TIME, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.async_connect_postgres import Base

metadata = sqlalchemy.MetaData()


class SendSetting(Base):
    __tablename__ = 'send_settings'
    id = Column(Integer, primary_key=True, index=True)
    type_event = Column(String(256), )
    instant_delivery = Column(Boolean, default=False)
    periodic_time = Column(Integer, nullable=True)
    work_time_start = Column(TIME, )
    work_time_finish = Column(TIME, )
    user_id = Column(Integer, ForeignKey('users.user_id'))

    user = relationship('User', back_populates='settings')

    class Config:
        orm_mode = True
