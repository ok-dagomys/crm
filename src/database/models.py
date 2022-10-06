from sqlalchemy import Column, Boolean, Integer, String

from src.database.sql import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(50), unique=True)
    password = Column(String(100))
    is_admin = Column(Boolean, default=False)
