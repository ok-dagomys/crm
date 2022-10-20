import filecmp
import logging
import os
import shutil
import time

import pandas as pd
from tqdm import tqdm

from cfg import phonebook_source, phonebook_destination
from src.database.sql import engine


def scan_phonebook():
    if not os.path.exists(phonebook_destination) or not filecmp.cmp(phonebook_source, phonebook_destination):
        logging.info('Phonebook has a new version on server')

        shutil.copy2(phonebook_source, phonebook_destination, follow_symlinks=False)
        with tqdm(total=100) as pbar:
            for i in range(10):
                time.sleep(0.1)
                pbar.update(10)
                pbar.set_description("Copying...")
        filecmp.clear_cache()

        status = 'Updated'
    else:
        status = 'Actual'
    return status


def filter_phonebook():
    xl = pd.ExcelFile(phonebook_destination)
    sheets = xl.sheet_names
    sheets.remove('Тетьково')

    df = pd.DataFrame()
    rem_words = ['Столбец1', 'Столбец2', 'Столбец3', 'Столбец4', 'Столбец5', 'Столбец6', 'Столбец7',
                 'Фамилия', 'Имя Отчество', 'Должность', 'Отдел (служба)', 'СО № 7',
                 'Внутренний телефон', 'Городской телефон', 'Мобильный телефон']
    for sheet in sheets:
        data = pd.read_excel(xl, sheet_name=sheet, header=None, index_col=None)
        # df = df.append(data)
        df = pd.concat([df, data])
    for word in rem_words:
        df = df.mask(df == word)
    xl.close()

    df = df[[1, 2, 3, 4, 5, 6, 7]].dropna(axis=0, how='all')
    df = df[[1, 2, 3, 4, 5, 6, 7]].fillna('', axis=1)
    df.columns = ['name', 'surname', 'role', 'department', 'number', 'work', 'mobile']
    df = df.replace('-', '', regex=True).astype(str).reset_index(drop=True)
    df = df.drop(df[(df['number'] == '') & (df['work'] == '') & (df['mobile'] == '')]
                 .index, axis=0).reset_index(drop=True)

    def column_filter(column_name):
        if column_name in ['number', 'work', 'mobile']:
            df[column_name] = df[column_name].apply(lambda x: x.replace('(факс)', '').split())
            df[column_name] = df[column_name].apply(lambda x: ','.join(map(str, x)).replace(',', ', '))
        else:
            df[column_name] = df[column_name].apply(lambda x: x.split())
            df[column_name] = df[column_name].apply(lambda x: ' '.join(map(str, x)).replace('"', "'"))

    for name in df.columns:
        column_filter(name)
    return df


def phonebook_from_sql():
    with engine.begin() as connection:
        df = pd.read_sql('phonebook', con=connection, index_col='index').reset_index(drop=True)
    return df


# scan_phonebook()
df1 = filter_phonebook()
df2 = phonebook_from_sql()

df_diff = pd.concat([df1, df2]).drop_duplicates(keep=False)
print(df_diff)
