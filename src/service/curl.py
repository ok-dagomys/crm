import json
from datetime import datetime

import requests
from requests.structures import CaseInsensitiveDict

from src.database.models import WeatherModel, CovidModel
from src.database.sql import SessionLocal


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