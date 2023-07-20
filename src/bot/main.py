import asyncio
from asyncio import set_event_loop, new_event_loop

import aioschedule

from cfg import date_time
from src.bot.telegram import bot_run, edit_message, send_message, delete_message
from src.database.sql import check_table_exist
from src.service.bot import find_pined_message_id
from src.service.covid import check_covid_status, covid_to_db
from src.service.phonebook import edit_new_call, check_call_status, edit_answered_call
from src.service.tasks import task_new_status
from src.service.weather import check_weather_status, weather_to_db


async def check_weather():
    if check_table_exist('weather'):
        forecast, status = check_weather_status()
        if status == 'new':
            try:
                await edit_message(forecast, find_pined_message_id())
                weather_to_db(forecast, 'send')
            except Exception as ex:
                print(f'Weather {date_time()} | {ex}\n')
    await asyncio.sleep(0.1)


async def check_covid():
    if check_table_exist('covid'):
        prognosis, status = check_covid_status()
        if status == 'new':
            try:
                await send_message(prognosis)
                covid_to_db(prognosis, 'send')
            except Exception as ex:
                print(f'Covid {date_time()} | {ex}\n')
    await asyncio.sleep(0.1)


async def check_tasks():
    if check_table_exist('tasks'):
        task = task_new_status()
        if task:
            try:
                await send_message(f'{task[1]} - {task[2]}')
            except Exception as ex:
                print(f'Task {date_time()} | {ex}\n')
    await asyncio.sleep(0.1)


async def check_calls():
    if check_table_exist('calls'):
        numbers = check_call_status('new')
        if numbers:
            try:
                message_id = await send_message(
                    f'Incoming call\n'
                    f'from number: {numbers[0]}\n'
                    f'to number: {numbers[1]}')
                edit_new_call('dial', message_id, numbers[0])
            except Exception as ex:
                print(f'Calls {date_time()} | {ex}\n')
        else:
            message_id = check_call_status('answered')
            if message_id and message_id[0].isdigit():
                try:
                    await delete_message(message_id[0])
                    edit_answered_call(message_id[0])
                except Exception as ex:
                    print(f'Calls {date_time()} | {ex}\n')
    await asyncio.sleep(0.1)


async def scheduler():
    # aioschedule.every(5).to(10).seconds.do(check_weather)
    # aioschedule.every(5).to(10).seconds.do(check_covid)
    aioschedule.every(5).to(10).seconds.do(check_tasks)
    aioschedule.every(1).to(3).seconds.do(check_calls)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(0.1)


async def tasks():
    asyncio.create_task(scheduler())
    await asyncio.sleep(0.1)


set_event_loop(new_event_loop())
asyncio.get_event_loop().run_until_complete(tasks())

if __name__ == '__main__':
    bot_run()
