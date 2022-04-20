from datetime import time, datetime
from typing import Optional

from pydantic import BaseModel, Field


class EventSetting(BaseModel):
    type_event: str = Field(..., example='test event')
    instant_delivery: bool = Field(default=False, )
    periodic_time: int = Field(default=15, )
    work_time_start: time = Field(default="09:00:00", )
    work_time_finish: time = Field(default="09:00:00", )
    last_send: datetime = Field(default="2022-04-20T12:00:00", )
    user_id: int = Field(..., example=99)


class EventSettingUpdateSchema(BaseModel):
    type_event: str = Field(..., example='test event')
    instant_delivery: bool = Field(default=False, )
    periodic_time: int = Field(default=15, )
    work_time_start: time = Field(default="09:00:00", )
    work_time_finish: time = Field(default="09:00:00", )
