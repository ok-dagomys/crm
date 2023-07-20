import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


def date_time():
    date = datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M:%S')
    return date, time


def check_workdir():
    local_path = os.getenv('LOCAL_PROJECT')
    if local_path in os.getcwd():
        return 'local'


# Asterisk
ami_host = os.getenv('AMI_HOST')
ami_port = os.getenv('AMI_PORT')
ami_username = os.getenv('AMI_USERNAME')
ami_secret = os.getenv('AMI_SECRET')


# MySql
sql_user = os.getenv('SQL_USER')
sql_password = os.getenv('SQL_PASSWORD')
sql_database = os.getenv('SQL_DATABASE')
if check_workdir() == 'local':
    sql_host = os.getenv('LOCAL_SQL_HOST')
    sql_port = os.getenv('LOCAL_SQL_PORT')
else:
    sql_host = os.getenv('DOCKER_SQL_HOST')
    sql_port = os.getenv('DOCKER_SQL_PORT')


# FastAPI
if check_workdir() == 'local':
    api_host = os.getenv('LOCAL_FASTAPI_HOST')
    api_port = os.getenv('LOCAL_FASTAPI_PORT')
else:
    api_host = os.getenv('DOCKER_FASTAPI_HOST')
    api_port = os.getenv('DOCKER_FASTAPI_PORT')


# Telegram bot
id_list = []
if check_workdir() == 'local':
    bot_token = os.getenv('PRIVATE_TOKEN')
    bot_id = os.getenv('PRIVATE_ID')
else:
    bot_token = os.getenv('GROUP_TOKEN')
    bot_id = os.getenv('GROUP_ID')


# Tasks
if check_workdir() == 'local':
    task_source = os.getenv('LOCAL_TASK_SOURCE')
    task_registry = os.getenv('LOCAL_TASK_REGISTRY')
    task_archive = os.getenv('LOCAL_TASK_ARCHIVE')
else:
    task_source = os.getenv('DOCKER_TASK_SOURCE')
    task_registry = os.getenv('DOCKER_TASK_REGISTRY')
    task_archive = os.getenv('DOCKER_TASK_ARCHIVE')


# Phonebook
if check_workdir() == 'local':
    phonebook_source = os.getenv('LOCAL_PHONEBOOK_SOURCE')
    phonebook_destination = os.getenv('LOCAL_PHONEBOOK_DESTINATION')
else:
    phonebook_source = os.getenv('DOCKER_PHONEBOOK_SOURCE')
    phonebook_destination = os.getenv('DOCKER_PHONEBOOK_DESTINATION')

