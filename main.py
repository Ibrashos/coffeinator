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
from aiogram.types.web_app_info import WebAppInfo



import sqlite3 as sq

from dotenv import load_dotenv

import ChatGPT as gpt


load_dotenv()
bot = Bot(os.getenv("TOKEN_TGBOT"), parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)




def request_to_user_db(sql):
    with sq.connect("cofe_table.db") as con:  # подключение к базе данных
        cur = con.cursor()  # создание объекта для работы с базой данных
        cur.execute(sql)
        result = cur.fetchall()
        return result


def check_user(mes):
    sql = 'SELECT tg_id FROM users'
    check = request_to_user_db(sql)
    a = []
    for res in check:
        for x in res:
            a.append(x)
    if mes.chat.id in a:
        return 2
    else:
        return 1


def add_order(mes, data):  #Добавление заказа в БД
    request_to_user_db("""INSERT INTO korzina (tg_id,item) VALUES (?,?)""",(mes.chat.id, data))
    if check_user(mes) == 1:
        request_to_user_db("""INSERT INTO users (tg_id) VALUES (?)""", (mes.chat.id))


def list_product(num):
    items = {'cofe1':{'espresso': 'Экспрессо', 'price': '160'},
             'cofe2':{'latte': 'Латте', 'price': '250'},
             'cofe3':{'americano': 'Американо', 'price': '180'}}
    topings = {'toping1':{'milk': 'Молоко', 'price': '30'},
               'toping2':{'slivki': 'Сливки', 'price': '20'},
               'toping3':{'kakao': 'Какао', 'price': '50'},
               'toping4':{'cinnamon': 'Корица', 'price': '10'}}
    if num == 1:
        return items
    else: return topings


class SomeState(StatesGroup):
    waiting_ai = State()
    item_wait = State()




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
    markup.add('Меню','FAQ')
    check = request_to_user_db(f'SELECT * FROM users WHERE tg_id = {message.chat.id}')
    try:
        check = check[0][2]
    except IndexError:
        with sq.connect("cofe_table.db") as con:  # подключение к базе данных
            cur = con.cursor()  # создание объекта для работы с базой данных
            cur.execute("""INSERT INTO users (tg_id,privilages) VALUES (?,?)""", (message.chat.id, 'Client'))
    check = request_to_user_db(f'SELECT * FROM users WHERE tg_id = {message.chat.id}')
    if check[0][2].lower() == 'admin':
        markup.add('Заказы')
        await bot.send_message(message.chat.id, f"Я бот бариста команды Престиж \n\nЗдесь вы можете максимально удобно и быстро пользоваться продукцией сети кофеен \n\n Нажимайте кнопку «Старт» и начинайте пользоваться ботом. Приятного аппетита ☕️🍩", reply_markup=markup)
    else:
        await bot.send_message(message.chat.id, f"Я бот бариста команды Престиж \n\nЗдесь вы можете максимально удобно и быстро пользоваться продукцией сети кофеен \n\n Нажимайте кнопку «Старт» и начинайте пользоваться ботом. Приятного аппетита ☕️🍩", reply_markup=markup)


@dp.message_handler(commands='cancel')
async def cancel_handler(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Меню', 'FAQ')
    await message.reply('Операция отменена', reply_markup=markup)


# МЕНЮ МЕНЮ МЕНЮ МЕНЮ МЕНЮ МЕНЮ МЕНЮ МЕНЮ МЕНЮ
@dp.message_handler()
async def message_handler(message: types.Message):
    if message.text.lower() == 'меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Кофе','Добавки','Назад')
        kb = InlineKeyboardMarkup(row_width=1)
        button = InlineKeyboardButton(text="Перейти", web_app=WebAppInfo(url='https://gvbu3gxzfunovqryq18fow.on.drv.tw/projects/live_1/'))
        kb.add(button)
        await message.answer("Выберите что то из списка", reply_markup=kb)



    if message.text.lower() == 'заказы':
        check = request_to_user_db(f'SELECT * FROM users WHERE tg_id = {message.chat.id}')
        check = check[0][2]
        if check.lower() == 'admin':
            result = request_to_user_db(f'SELECT tg_id FROM korzina')
            a = []
            for num in result:
                for i in num:
                    if i not in a:
                        a.append(i)
            result = a
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            kb = InlineKeyboardMarkup(row_width=1)
            for res in result:
                markup.add(str(res))
            await message.answer('Выгрузка заказов...', reply_markup=markup)
            await message.answer('Какой заказ вас интересует?', reply_markup=kb.add(InlineKeyboardButton(text='Отмена⛔', callback_data='cancel_adm')))
            await SomeState.item_wait.set()



    # FAQ FAQ FAQ FAQ FAQ FAQ FAQ FAQ FAQ FAQ FAQ FAQ
    if message.text.lower() == 'faq':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('FAQ')
        item = faq()
        kb = InlineKeyboardMarkup(row_width=1)

        for key, value in item.items():
            button = InlineKeyboardButton(text=value, callback_data=key)

            kb.add(button)
        button = InlineKeyboardButton(text='Спросить у ИИ ↗', callback_data='ai')
        kb.add(button)
        await bot.send_message(message.chat.id, "Частые вопросы:", reply_markup=kb)

    # НАЗАД НАЗАД НАЗАД НАЗАД НАЗАД НАЗАД НАЗАД НАЗАД
    if message.text.lower() == 'назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Меню', 'FAQ')
        check = request_to_user_db(f'SELECT * FROM users WHERE tg_id = {message.chat.id}')
        check = check[0][2]
        if check.lower() == 'admin':
            markup.add('Заказы')
            await bot.send_message(message.chat.id, "Приветствую", reply_markup=markup)
        else:
            await bot.send_message(message.chat.id, "Приветствую", reply_markup=markup)
@dp.message_handler(state=SomeState.item_wait)
async def handle_message(message: Message, state: FSMContext):
    check = request_to_user_db(f'SELECT * FROM korzina WHERE tg_id == {message.chat.id}')
    a = []
    kb = InlineKeyboardMarkup(row_width=1)
    for res in check:
        print(res)
        a.append(res[2])
    for i in a:
        kb.add(InlineKeyboardButton(text=f"☕️{i}", callback_data=i))
    # Обработка сообщения от пользователя
    await bot.send_message(message.chat.id, 'Заказы пользователя:', reply_markup=kb)
    # Сброс состояния FSM
    await state.finish()

# ОТВЕТЫЫЫ на FAQ
@dp.callback_query_handler(Text("question1"))
async def send_answer(callback: types.CallbackQuery):
    await callback.message.answer('Широкий ассортимент кофейных напитков, включая эспрессо, капуччино, латте, американо, макиато и другие напитки')
@dp.callback_query_handler(Text("question2"))
async def send_answer(callback: types.CallbackQuery):
    await callback.message.answer('Различные виды молока, сливки, ванильный сироп, кокосовую стружку и многое другое')
@dp.callback_query_handler(Text("question3"))
async def send_answer(callback: types.CallbackQuery):
    await callback.message.answer('Наша кофейня работает с 8:00 утра до 10:00 вечера с понедельника по пятницу, и с 9:00 утра до 9:00 вечера в выходные')


@dp.callback_query_handler(Text("ai"))
async def button_pressed_handler(callback: types.CallbackQuery, state: FSMContext):
    # Обработка нажатия кнопки
    await callback.answer("Напишите свой вопрос")
    # Получение данных из callback_data
    button_data = callback.data
    # Сохранение данных в состояние FSM
    await state.update_data(button_data=button_data)
    # Ожидание следующего сообщения от пользователя
    await SomeState.waiting_ai.set()


@dp.message_handler(state=SomeState.waiting_ai)
async def handle_message(message: Message, state: FSMContext):
    # Обработка сообщения от пользователя
    button_data = (await state.get_data())["button_data"]
    await bot.send_message(message.chat.id, 'Ответ генерируется...')
    await message.answer(f"Ваш ответ на вопрос: {gpt.chat(text=message.text)}")
    kb = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text='Спросить у ИИ ↗', callback_data='ai')
    kb.add(button)
    await bot.send_message(message.chat.id, "Задать вопрос ещё раз", reply_markup=kb)
    # Сброс состояния FSM
    await state.finish()


@dp.callback_query_handler(Text('cancel'))
async def send_answer(callback: types.CallbackQuery):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Меню', 'FAQ')
    await bot.send_message(callback.message.chat.id, 'Операция отменена', reply_markup=markup)


#МЕНЯЯЯЯТЬ
@dp.callback_query_handler(Text('cancel_adm'))
async def send_answer(callback: types.CallbackQuery,state:FSMContext):
    await state.finish()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Меню', 'FAQ')
    markup.add('Заказы')
    await bot.send_message(callback.message.chat.id, "Приветствуем", reply_markup=markup)




async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("Бот в сети...")
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except BaseException:
        print("Error")

# Button = InlineKeyboardButton(text='Перейти в блог Skillbox', url='https://skillbox.ru/media/code/')
# Button2 = InlineKeyboardButton(text='Перейти к курсам Skillbox', url='https://skillbox.ru/code/')



