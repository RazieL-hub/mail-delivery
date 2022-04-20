from datetime import datetime

from pydantic import BaseModel
from pydantic.types import Json


class ReportSchema(BaseModel):
    user_id: int
    type_event: str
    report_data: Json
    count: int
    date_time: datetime
    status: bool = False
