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
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

import sqlite3 as sq

from dotenv import load_dotenv

load_dotenv()
bot = Bot(os.getenv("TOKEN_TGBOT"), parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def coffe():
    items = ['Эспрессо', 'Каппучино', 'Латте', 'Американо']
    return items


def faq():
    items = {
        'question1': 'Какие кофейные напитки вы предлагаете?',
        'question2': 'Какие добавки и сиропы у вас есть для кофе?',
        'question3': 'Каковы ваши рабочие часы?'
    }
    return items


@dp.message_handler(commands=["start"])
async def command_start_handler(message: Message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = f"Меню"
    item2 = f"FAQ"
    markup.add(item1, item2)
    await bot.send_message(message.chat.id, "Приветствую", reply_markup=markup)


@dp.message_handler(commands='cancel')
async def cancel_handler(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Меню', 'FAQ')
    await message.reply('Операция отменена', reply_markup=markup)


# МЕНЮ МЕНЮ МЕНЮ МЕНЮ МЕНЮ МЕНЮ МЕНЮ МЕНЮ МЕНЮ
@dp.message_handler()
async def message_handler(message: types.Message):
    if message.text.lower() == 'меню':
        items = coffe()
        markup = types.ReplyKeyboardMarkup()
        for item in items:
            markup.add(item)
        await bot.send_message(message.chat.id, "Выберите кофе на заказ или вернитесь в начало. /cancel",
                               reply_markup=markup)


# FAQ FAQ FAQ FAQ FAQ FAQ FAQ FAQ FAQ FAQ FAQ FAQ
    if message.text.lower() == 'faq':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Назад')
        item = faq()
        kb = InlineKeyboardMarkup(row_width=1)

        for key, value in item.items():
            button = InlineKeyboardButton(text=value, callback_data=key)


            kb.add(button)
        await bot.send_message(message.chat.id, "Частые вопросы:", reply_markup=kb)


# НАЗАД НАЗАД НАЗАД НАЗАД НАЗАД НАЗАД НАЗАД НАЗАД
    if message.text.lower() == 'назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Меню', 'FAQ')
        await bot.send_message(message.chat.id, "Выберите кофе на заказ или вернитесь в начало. /cancel",
                               reply_markup=markup)

# @dp.callback_query(Text('question1'))
# async def send_answer(callback: types.CallbackQuery):
#     await callback.message.answer('Ответ')

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())




 # Button = InlineKeyboardButton(text='Перейти в блог Skillbox', url='https://skillbox.ru/media/code/')
 # Button2 = InlineKeyboardButton(text='Перейти к курсам Skillbox', url='https://skillbox.ru/code/')