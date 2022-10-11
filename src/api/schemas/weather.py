from datetime import datetime

from pydantic import BaseModel


class WeatherCreate(BaseModel):
    forecast: str


class Weather(WeatherCreate):
    id: int
    date: datetime

    class Config:
        orm_mode = True
