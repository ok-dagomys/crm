import pandas as pd

from cfg import date_time
from src.database.sql import engine


def covid_status(prognosis):
    with engine.begin() as connection:
        df = pd.read_sql('covid', con=connection)
        if df['prognosis'].values[0] != prognosis:
            return 'new'


def check_covid_status():
    with engine.begin() as connection:
        df = pd.read_sql('covid', con=connection)
        prognosis = df['prognosis'].values[0]
        status = df['status'].values[0]
        return prognosis, status


def covid_to_db(prognosis, status):
    with engine.begin() as connection:
        covid = [[status, prognosis, date_time()[0], date_time()[1]]]
        df = pd.DataFrame(covid, columns=['status', 'prognosis', 'date', 'time'])
        df.to_sql('covid', con=connection, if_exists='replace', index=False)
