import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from cfg import bot_token, bot_id, id_list, date_time
from src.service.bot import drop_bot_table, bot_to_db
from src.service.phonebook import name_recognition

logging.basicConfig(level=logging.WARNING)
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


async def fn(_):
    print('Aiogram bot')


async def send_message(message):
    bot_message = await bot.send_message(bot_id, message)
    message_id = bot_message.message_id
    id_list.append(message_id)
    bot_to_db(message, message_id)
    await asyncio.sleep(1)
    print(f"{date_time()} | Bot send message (id: {message_id})")
    return message_id


async def edit_message(message, message_id):
    await bot.edit_message_text(message, bot_id, message_id)
    print(f"{date_time()} | Bot edit message (id: {message_id})")
    await asyncio.sleep(1)


async def delete_message(message_id):
    await bot.delete_message(bot_id, message_id)
    print(f"{date_time()} | Bot delete message (id: {message_id})")
    await asyncio.sleep(1)


async def pin_message(message_id):
    await bot.pin_chat_message(bot_id, message_id)
    print(f"{date_time()} | Bot pin message (id: {message_id})")
    await asyncio.sleep(1)


@dp.message_handler(commands=['test'])
async def bot_answer(message: types.Message):
    await send_message('Тест пройден!')
    await message.delete()
    await asyncio.sleep(1)


# delete all pinned message
@dp.message_handler(content_types=['pinned_message'])
async def delete_pinned(message: types.Message):
    print(f"{date_time()} | Bot delete pinned_message")
    await message.delete()


@dp.message_handler(commands=['?'])
async def bot_answer(message: types.Message):
    search = await name_recognition(message.text)
    await send_message(search)
    await message.delete()
    await asyncio.sleep(0.1)


async def on_startup(_):
    message_id = await send_message('Бот приступил к работе!')
    # await pin_message(message_id)
    logging.warning('Bot start working')
    await asyncio.sleep(1)


async def on_shutdown(_):
    # for message_id in id_list:
    #     await delete_message(message_id)
    drop_bot_table()
    await asyncio.sleep(1)


def bot_run(startup=fn, shutdown=fn):
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=(on_startup, startup),
                           on_shutdown=(on_shutdown, shutdown))

