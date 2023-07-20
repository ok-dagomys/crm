import pandas as pd
from sqlalchemy import text

from cfg import date_time
from src.database.sql import engine, check_table_exist


def find_pined_message_id():
    if check_table_exist('bot'):
        with engine.begin() as connection:
            df = pd.read_sql('bot', con=connection)
            return df['message_id'].values[0]
    else:
        return '0000'


def bot_to_db(data, message_id):
    with engine.begin() as connection:
        bot = [[data, message_id, date_time()[0], date_time()[1]]]
        df = pd.DataFrame(bot, columns=['logs', 'message_id', 'date', 'time'])
        df.to_sql('bot', con=connection, if_exists='append', index=False)


def drop_bot_table():
    with engine.connect() as connection:
        connection.execute(text("DROP TABLE bot"))
