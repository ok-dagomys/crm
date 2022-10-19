import json
from datetime import datetime

import pandas as pd
import requests
from fastapi import HTTPException
from requests.structures import CaseInsensitiveDict

from src.database.models import WeatherModel, CovidModel
from src.database.sql import SessionLocal, engine


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


def send_curl(data_dict, route):
    url = f"http://api:8000/{route}"

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    data = json.dumps(data_dict)

    return requests.post(url, headers=headers, data=data)


def weather_to_db(data):
    with SessionLocal.begin() as session:
        check_model = session \
            .query(WeatherModel) \
            .order_by(WeatherModel.id.desc()) \
            .filter_by(forecast=data).first()
        if not check_model:
            # session.add(WeatherModel(forecast=data))
            send_curl(data_dict={"forecast": data}, route='weather')
        else:
            if check_model.date.strftime("%Y.%m.%d") < datetime.now().strftime("%Y.%m.%d"):
                send_curl(data_dict={"forecast": data}, route='weather')


def covid_to_db(data):
    with SessionLocal.begin() as session:
        check_model = session \
            .query(CovidModel) \
            .order_by(CovidModel.id.desc()) \
            .filter_by(prognosis=data).first()
        if not check_model:
            send_curl(data_dict={"prognosis": data}, route='covid')
        else:
            if check_model.date.strftime("%Y.%m.%d") < datetime.now().strftime("%Y.%m.%d"):
                send_curl(data_dict={"prognosis": data}, route='covid')


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
