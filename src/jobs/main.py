import asyncio

import aioschedule

from covid import check_covid_info
from weather import check_weather
from phonebook import check_phonebook
from tasks import check_task


async def scheduler():
    aioschedule.every(1).to(2).minutes.do(check_task)
    aioschedule.every(2).to(3).minutes.do(check_weather)
    aioschedule.every(3).to(4).minutes.do(check_phonebook)
    aioschedule.every(5).to(5).minutes.do(check_covid_info)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(0.1)


async def pending():
    task = asyncio.create_task(scheduler())
    await task
    await asyncio.sleep(0.1)


if __name__ == '__main__':
    asyncio.run(pending())
