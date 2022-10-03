import asyncio

import aioschedule

from covid import check_covid_info
from phonebook import check_phonebook
from tasks import check_task


async def scheduler():
    aioschedule.every(1).to(5).minutes.do(check_task)
    aioschedule.every(1).to(5).minutes.do(check_phonebook)
    aioschedule.every(1).to(5).minutes.do(check_covid_info)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(0.1)


async def pending():
    task = asyncio.create_task(scheduler())
    await task
    await asyncio.sleep(0.1)


if __name__ == '__main__':
    asyncio.run(pending())
