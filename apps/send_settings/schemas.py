from datetime import time, datetime
from typing import Optional

from pydantic import BaseModel, Field


class SendSettingsSchema(BaseModel):
    type_event: str = Field(..., example='Событие счётчика')
    instant_delivery: bool = Field(default=False, example='True', description='INSTANT OR DELAY')
    periodic_time: int = Field(default=15, example=5,
                               description="Please, enter value in minutes. Default = 15 minutes")
    work_time_start: time = Field(None, example='09:00:00',
                                  description='Please, enter value like example')
    work_time_finish: time = Field(None, example='18:00:00',
                                   description='Please, enter value like example')
    user_id: int = Field(..., description='User_id to whom to apply this settings. This field is required')


class SendSettingsUpdateSchema(BaseModel):
    type_event: str = Field(..., example='Событие счётчика')
    instant_delivery: bool = Field(default=False, description='INSTANT OR DELAY')
    periodic_time: int = Field(default=15, example=5,
                               description="Please, enter value in minutes. Default = 15 minutes")
    work_time_start: time = Field(default='09:00:00', example='09:00:00',
                                  description='Please, enter value like example')
    work_time_finish: time = Field(default='18:00:00', example='18:00:00',
                                   description='Please, enter value like example')
