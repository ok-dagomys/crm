from sqlalchemy import Column, Boolean, Integer, String, DateTime, func

from src.database.sql import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(50), unique=True)
    password = Column(String(100))
    is_admin = Column(Boolean, default=False)


class WeatherModel(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    forecast = Column(String(50))
    date = Column(DateTime, default=func.now())
