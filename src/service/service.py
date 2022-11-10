from datetime import datetime

import pandas as pd
from fastapi import HTTPException

from src.database.sql import engine


def check_exist_in_db(db, model, model_filter, schema_filter):
    db_model = db.query(model).filter(model_filter == schema_filter).first()
    if db_model:
        raise HTTPException(status_code=304, detail="No changes")


def check_name_exist_in_db(db, schema, model):
    db_model = db.query(model).filter(model.name == schema.name).first()
    if db_model:
        raise HTTPException(status_code=302, detail=f"{schema.name} already exist")


def add_to_db(db, model, new_model):
    if isinstance(new_model, model):
        db.add(new_model)
        db.commit()
        db.refresh(new_model)


def phonebook_to_db(df):
    with engine.begin() as connection:
        df.to_sql('phonebook', con=connection, if_exists='replace')


def task_to_db(file, status):
    with engine.begin() as connection:
        tasks = [[file, status, datetime.now().strftime("%Y.%m.%d-%H:%M:%S")]]
        df = pd.DataFrame(tasks, columns=['file', 'status', 'date'])
        df.to_sql('tasks', con=connection, if_exists='append', index=False)


def call_to_db(caller, number):
    with engine.begin() as connection:
        calls = [[caller, number, datetime.now().strftime("%Y.%m.%d-%H:%M:%S")]]
        df = pd.DataFrame(calls, columns=['from_number', 'to_number', 'date'])
        df.to_sql('calls', con=connection, if_exists='append', index=False)


async def caller_recognition(caller, number):
    with engine.begin() as connection:
        df = pd.read_sql('calls', con=connection)

    recognition = df[df['number'].str.contains(caller)]

    if recognition.shape[0] > 0:
        return f'Входящий звонок\nс номера: {caller}\nна номер: {number}' \
               f'\nот: {recognition.iloc[0]["role"]}\n{recognition.iloc[0]["name"]} {recognition.iloc[0]["surname"]}\n'
    else:
        return f'Входящий звонок\nс номера: {caller}\nна номер: {number}'


async def name_recognition(text):
    with engine.begin() as connection:
        df = pd.read_sql('phonebook', con=connection)
    search_name = text.split()
    name = search_name[1].strip().lower().title()
    recognition = df[df['name'].str.contains(name)]
    if recognition.shape[0] > 0:
        return f'ФИО: {recognition.iloc[0]["name"]} {recognition.iloc[0]["surname"]}\n'\
               f'Должность: {recognition.iloc[0]["role"]}\n'\
               f'Отдел: {recognition.iloc[0]["department"]}\n'\
               f'Внутренний: {recognition.iloc[0]["number"]}\n'\
               f'Рабочий: {recognition.iloc[0]["work"]}\n'\
               f'Мобильный: {recognition.iloc[0]["mobile"]}\n'
    else:
        return f'Совпадений по запросу "{name}" не найдено'
