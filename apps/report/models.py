import sqlalchemy
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from database.async_connect_postgres import Base

metadata = sqlalchemy.MetaData()


class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True, index=True)
    report_data = Column(JSONB, )
    date_created = Column(DateTime, server_default=now())
    status_send = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    type_event_id = Column(Integer, ForeignKey('events_config.id'))

    users = relationship('User', back_populates='user_reports')
    event_id = relationship('EventSetting', back_populates='event_settings')

    class Config:
        orm_mode = True
