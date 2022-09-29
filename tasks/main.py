import asyncio

import aioschedule

from purchase import check_task


async def scheduler():
    aioschedule.every(1).to(5).minutes.do(check_task)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(0.1)


async def pending():
    task = asyncio.create_task(scheduler())
    await task
    await asyncio.sleep(0.1)


if __name__ == '__main__':
    asyncio.run(pending())
