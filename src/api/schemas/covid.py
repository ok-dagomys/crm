from datetime import datetime

from pydantic import BaseModel


class CovidCreate(BaseModel):
    prognosis: str


class Covid(CovidCreate):
    id: int
    date: datetime

    class Config:
        orm_mode = True
