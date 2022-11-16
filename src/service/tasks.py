import pandas as pd
from sqlalchemy import text

from cfg import date_time
from src.database.sql import engine


def task_to_db(status, file, action):
    with engine.begin() as connection:
        tasks = [[status, file, action, date_time()]]
        df = pd.DataFrame(tasks, columns=['status', 'file', 'action', 'date'])
        df.to_sql('tasks', con=connection, if_exists='append', index=False)


def edit_status():
    with engine.begin() as connection:
        connection.execute(text("UPDATE tasks SET status = 'send' WHERE status = 'new' LIMIT 1"))


def task_new_status():
    with engine.begin() as connection:
        task = connection.execute(text("select * from tasks where status = 'new'")).first()
        edit_status()
        return task
