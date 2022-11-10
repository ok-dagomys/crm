import asyncio
import logging
from asyncio import set_event_loop, new_event_loop

import aioschedule

from cfg import date_time
from src.bot.telegram import bot_run, edit_message, send_message
from src.database.sql import check_table_exist
from src.service.bot import find_pined_message_id
from src.service.covid import check_covid_status, covid_to_db
from src.service.weather import check_weather_status, weather_to_db


async def check_weather():
    if check_table_exist('weather'):
        forecast, status = check_weather_status()
        if status == 'new':
            try:
                await edit_message(forecast, find_pined_message_id())
                weather_to_db(forecast, 'send')
            except Exception as ex:
                logging.info(f' {date_time()} | {ex}\n')
    await asyncio.sleep(0.1)


async def check_covid():
    if check_table_exist('covid'):
        prognosis, status = check_covid_status()
        if status == 'new':
            try:
                await send_message(prognosis)
                covid_to_db(prognosis, 'send')
            except Exception as ex:
                logging.info(f' {date_time()} | {ex}\n')
    await asyncio.sleep(0.1)


async def scheduler():
    aioschedule.every(5).to(10).seconds.do(check_weather)
    aioschedule.every(5).to(10).seconds.do(check_covid)
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
