from fastapi import Depends, Request, Response
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.orm import Session

from src.api.schemas.covid import Covid, CovidCreate
from src.api.schemas.users import User, UserCreate
from src.api.schemas.weather import Weather, WeatherCreate
from src.database.models import UserModel, WeatherModel, CovidModel
from src.service.service import add_to_db
from src.database.sql import get_db


def add_route(schema, create_schema, db_model, prefix, create_route=False):
    route = SQLAlchemyCRUDRouter(
        schema=schema,
        create_schema=create_schema,
        db_model=db_model,
        db=get_db,
        prefix=prefix,
        create_route=create_route,
        # dependencies=[Depends(AuthHandler().auth_wrapper)]
    )
    return route


users = add_route(User, UserCreate, UserModel, 'users')
weather = add_route(Weather, WeatherCreate, WeatherModel, 'weather')
covid = add_route(Covid, CovidCreate, CovidModel, 'covid')


@weather.post("", response_model=Weather, status_code=201)
def create_one(response: Response, request: Request, schema: WeatherCreate, db: Session = Depends(get_db)):
    forecast = WeatherModel(forecast=schema.forecast)
    add_to_db(db=db, model=WeatherModel, new_model=forecast)
    response.headers["Location"] = request.url._url
    return forecast


@covid.post("", response_model=Covid, status_code=201)
def create_one(response: Response, request: Request, schema: CovidCreate, db: Session = Depends(get_db)):
    prognosis = CovidModel(prognosis=schema.prognosis)
    add_to_db(db=db, model=CovidModel, new_model=prognosis)
    response.headers["Location"] = request.url._url
    return prognosis
