import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

load_dotenv()
sql_user = os.getenv('SQL_USER')
sql_password = os.getenv('SQL_PASSWORD')
sql_host = os.getenv('SQL_HOST')
sql_port = os.getenv('SQL_PORT')
sql_database = os.getenv('SQL_DATABASE')

engine = create_engine(
    url=f"mysql+pymysql://{sql_user}:{sql_password}@{sql_host}:{sql_port}/{sql_database}",
    echo=True)

meta = MetaData()

logs = Table(
    'logs', meta,
    Column('id', Integer, primary_key=True),
    Column('event', String(200)))


def add_to_db(new_event):
    meta.create_all(engine)
    ins = logs.insert().values(event=new_event)
    conn = engine.connect()
    conn.execute(ins)
    conn.close()
