import pandas as pd
from sqlalchemy import text

from cfg import date_time
from src.database.sql import engine


def call_to_db(status, caller, number):
    with engine.begin() as connection:
        calls = [[status, caller, number, date_time()[0], date_time()[1], 'not send']]
        df = pd.DataFrame(calls, columns=['status', 'from_number', 'to_number', 'date', 'time', 'message_id'])
        df.to_sql('calls', con=connection, if_exists='append', index=False)


def check_call_status(status):
    with engine.begin() as connection:
        if status == 'new':
            numbers = connection.execute(text(
                f"SELECT from_number, to_number "
                f"FROM calls "
                f"WHERE status = '{status}'")).first()
            return numbers
        elif status == 'answered':
            message_id = connection.execute(text(
                f"SELECT message_id "
                f"FROM calls "
                f"WHERE status = '{status}'")).first()
            return message_id


def edit_new_call(status, message_id, number):
    with engine.begin() as connection:
        connection.execute(text(
            f"UPDATE calls "
            f"SET status = '{status}', message_id = '{message_id}' "
            f"WHERE status = 'new' AND from_number = '{number}'"))


def edit_last_call(status):
    with engine.begin() as connection:
        number = connection.execute(text(
            f"SELECT from_number "
            f"FROM calls "
            f"ORDER BY date DESC")).first()[0]
        connection.execute(text(
            f"UPDATE calls "
            f"SET status = '{status}' "
            f"WHERE from_number = '{number}' AND date = '{date_time()[0]}'"))


def edit_answered_call(message_id):
    with engine.begin() as connection:
        connection.execute(text(
            f"UPDATE calls "
            f"SET status = 'processed', message_id = 'deleted' "
            f"WHERE message_id = '{message_id}'"))


def phonebook_to_db(df):
    with engine.begin() as connection:
        df.to_sql('phonebook', con=connection, if_exists='replace')


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
