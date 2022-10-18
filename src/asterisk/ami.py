import asyncio
import logging
import os
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from panoramisk import Manager, Message

from src.database.service import call_to_db

try:
    load_dotenv()
    manager = Manager(
        host=os.getenv('AMI_HOST'),
        port=os.getenv('AMI_PORT'),
        username=os.getenv('AMI_USERNAME'),
        secret=os.getenv('AMI_SECRET'),
        ping_delay=10,  # Delay after start
        ping_interval=10,  # Periodically ping AMI (dead or alive)
        reconnect_timeout=2)  # Timeout reconnect if connection lost
except Exception as ex:
    print(f'AMI-interface is not configured, or there is no connection. Error: {ex}')
finally:
    event, caller, number, status = [], [], [], []
    call = {}


def on_connect(mngr: Manager):
    logging.info('Connected to %s:%s AMI socket successfully' %
                 (mngr.config['host'], mngr.config['port']))


def on_login(mngr: Manager):
    logging.info('Connected user:%s to AMI %s:%s successfully' %
                 (mngr.config['username'], mngr.config['host'], mngr.config['port']))


def on_disconnect(mngr: Manager, exc: Exception):
    logging.info('Disconnect user:%s from AMI %s:%s' %
                 (mngr.config['username'], mngr.config['host'], mngr.config['port']))
    logging.debug(str(exc))


async def on_startup(mngr: Manager):
    await asyncio.sleep(0.1)
    logging.info('AMI-interface started')


async def on_shutdown(mngr: Manager):
    await asyncio.sleep(0.1)
    logging.info('Shutdown AMI connection on %s:%s' %
                 (mngr.config['host'], mngr.config['port']))


@manager.register_event('*')  # Register all events
async def ami_callback(mngr: Manager, msg: Message):
    if msg.Event == 'FullyBooted':
        event.append('AMI-interface started')


@manager.register_event('Newchannel')
async def callback(mngr: Manager, msg: Message):
    if msg.ChannelStateDesc == 'Down' and msg.Context != 'from-internal':
        if msg.CallerIDNum and msg.Exten:
            caller.append(msg.CallerIDNum)
            number.append(msg.Exten)
            call[msg.CallerIDNum] = 'dial'
            # print(call)
            logging.info(f'Incoming call\nfrom number: {msg.CallerIDNum}\nto number: {msg.Exten}')

            calls = [[msg.CallerIDNum, msg.Exten, datetime.now().strftime("%Y.%m.%d-%H:%M:%S")]]
            df = pd.DataFrame(calls, columns=['from_number', 'to_number', 'date'])
            call_to_db(df)
    await asyncio.sleep(1)


@manager.register_event('Dial')
async def callback(mngr: Manager, msg: Message):
    if msg.DialStatus == 'ANSWER':
        status.append('end')
        call[tuple(caller[:-1])] = 'end'
        # print(call)
        # print(msg)
        logging.info('Call ended')
    await asyncio.sleep(1)


def connect(state=True):
    logging.basicConfig(level=logging.INFO)
    manager.on_connect = on_connect
    manager.on_login = on_login
    manager.on_disconnect = on_disconnect
    manager.connect(run_forever=state, on_startup=on_startup, on_shutdown=on_shutdown)


connect()
