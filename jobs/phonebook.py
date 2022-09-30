import asyncio
import filecmp
import logging
import os
import shutil
from datetime import datetime

from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
dst = os.getenv('PHONEBOOK_DESTINATION')
src = os.getenv('PHONEBOOK_SOURCE')
date = datetime.now().strftime('%Y-%m-%d')
time = datetime.now().strftime('%H:%M:%S')
logging.basicConfig(level=logging.INFO)


async def scan_phonebook():
    if not os.path.exists(dst) or not filecmp.cmp(src, dst):
        logging.info('Phonebook has a new version on server')

        shutil.copy2(src, dst, follow_symlinks=False)
        with tqdm(total=100) as pbar:
            for i in range(10):
                await asyncio.sleep(0.1)
                pbar.update(10)
                pbar.set_description("Copying...")
        filecmp.clear_cache()

        status = 'Phonebook updated'
        logging.info(status)
    else:
        status = 'Phonebook is actual'
        logging.info(status)
    return status


async def check_phonebook():
    task = asyncio.create_task(scan_phonebook())
    await task
    logging.info(f' Last phonebook check | {datetime.now().strftime("%Y.%m.%d в %H:%M:%S")}')
    await asyncio.sleep(0.1)


asyncio.run(check_phonebook())
