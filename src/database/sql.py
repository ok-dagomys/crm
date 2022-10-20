from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from cfg import sql_user, sql_password, sql_host, sql_port, sql_database

sql_database_url = f"mysql+pymysql://{sql_user}:{sql_password}@{sql_host}:{sql_port}/{sql_database}"

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
