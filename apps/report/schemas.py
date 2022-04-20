from datetime import datetime

from pydantic import BaseModel, Field
from pydantic.types import Json


class ReportSchema(BaseModel):
    user_id: int
    type_event: str
    report_data: Json
    date_time: datetime = Field(..., example=datetime.now())
    status: bool = False
