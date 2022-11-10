import pandas as pd

from cfg import date_time
from src.database.sql import engine
from src.service.bot import find_pined_message_id


def weather_status(forecast):
    with engine.begin() as connection:
        df = pd.read_sql('weather', con=connection)
        if df['forecast'].values[0] != forecast:
            return 'new'


def check_weather_status():
    with engine.begin() as connection:
        df = pd.read_sql('weather', con=connection)
        forecast = df['forecast'].values[0]
        status = df['status'].values[0]
        return forecast, status


def weather_to_db(forecast, status):
    with engine.begin() as connection:
        weather = [[status, forecast, date_time(), find_pined_message_id()]]
        df = pd.DataFrame(weather, columns=['status', 'forecast', 'date', 'message_id'])
        df.to_sql('weather', con=connection, if_exists='replace', index=False)
