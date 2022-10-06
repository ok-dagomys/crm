import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
sql_user = os.getenv('SQL_USER')
sql_password = os.getenv('SQL_PASSWORD')
sql_host = os.getenv('SQL_HOST')
sql_port = os.getenv('SQL_PORT')
sql_database = os.getenv('SQL_DATABASE')
sql_database_url = f"mysql+pymysql://" \
                   f"{sql_user}:" \
                   f"{sql_password}@{sql_host}:" \
                   f"{sql_port}/" \
                   f"{sql_database}"

engine = create_engine(url=sql_database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()
