import asyncio
import logging
import os

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram import Bot, Dispatcher,types
from aiogram.types import Message
import sqlite3 as sq

from dotenv import load_dotenv

load_dotenv()
bot = Bot(os.getenv("TOKEN"), parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

def coffe():
    items = ['Эспрессо','Каппучино','Латте','Американо']
    return items

@dp.message_handler(commands=["start"])
async def command_start_handler(message: Message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = f"Меню"
    item2 = f"О нас"
    markup.add(item1, item2)
    await bot.send_message(message.chat.id, "Приветствую", reply_markup=markup)

@dp.message_handler()
async def message_handler(message: types.Message):
    if message.text.lower() == 'меню':
        items = coffe()
        markup = types.ReplyKeyboardMarkup()
        await bot.send_message(message.chat.id, reply_markup=)


















async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
