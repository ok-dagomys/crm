import json
from datetime import datetime

import requests
from fastapi import HTTPException
from requests.structures import CaseInsensitiveDict

from src.database.models import WeatherModel
from src.database.sql import SessionLocal


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
