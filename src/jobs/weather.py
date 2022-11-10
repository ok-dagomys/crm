import logging

import aiohttp
import asyncio

from cfg import date_time
from src.service.weather import weather_status, weather_to_db

logging.basicConfig(level=logging.INFO)


async def weather_request():
    async with aiohttp.ClientSession() as session:
        city = 'Sochi'  # Enter the name of your city here
        url = f'https://wttr.in/{city}'
        weather_parameters = {
            'format': 2,
            '0': '',
            'T': '',
            'M': '',
            'lang': 'ru'
        }
        try:
            async with session.get(url, params=weather_parameters, ssl=False) as response:
                forecast = await response.text() if response.status == 200 else f'Cannot connect to host: {url}'
                # print(f'Weather forecast {forecast} in {city}')
                await asyncio.sleep(0.1)
                forecast = 'test: ⛅ 🌡️+22°C 🌬️↑4.2m/s'
                return forecast

        except Exception as ex:
            print(f"weather_module: {ex}")


async def check_weather():
    task = asyncio.create_task(weather_request())
    await task
    if weather_status(task.result()) == 'new':
        weather_to_db(task.result(), 'new')
    logging.info(f' {date_time()} | Weather checked\n')
    await asyncio.sleep(0.1)


asyncio.run(check_weather())
