from pydantic import BaseModel


class ReportSchema(BaseModel):
    status: bool = False