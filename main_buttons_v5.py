import os

import logging
import asyncio
import sqlite3
import requests

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandObject, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, URLInputFile
from dotenv import load_dotenv
from aiogram import html
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from setting import config

logger = logging.getLogger(__name__)
# Bot token can be obtained via https://t.me/BotFahter

load_dotenv()

# Dispatcher is a root router
dp = Dispatcher()

# All handlers should be attached to the Router (or Dispatcher)
router = Router()

con = sqlite3.connect(config.db_name)
cursor = con.cursor()

api_key = (config.api_key.get_secret_value())


class CurrencyState(StatesGroup):
    first_select = State()
    second_select = State()


def create_table():
    text = """
        CREATE TABLE IF NOT EXISTS currency (
            id integer PRIMARY KEY,
            from_currency TEXT NOT NULL,
            to_currency TEXT NOT NULL,
            created_at TEXT,
            UNIQUE(from_currency,to_currency)
        );
    """
    response = cursor.execute(text)


def clear_table():
    text = "DELETE FROM currency;"
    response = cursor.execute(text)
    con.commit()


def insert_currency(curr_from: str, curr_to: str):
    text = f"""
        INSERT INTO currency (from_currency, to_currency, created_at)
        VALUES ('{curr_from}', '{curr_to}', datetime('now'));
    """
    response = cursor.execute(text)
    con.commit()


def add_currency_data():
    #insert_currency("USD", "UAH")
    #insert_currency("USD", "EUR")
    #insert_currency("USD", "GBP")
    base_currencies = ["UAH", "JPY", "CAD", "USD", "EUR", "GBP"]
    target_currencies = ["USD", "EUR", "GBP", "UAH", "JPY", "CAD"]
    for base_currency in base_currencies:
        for target_currency in target_currencies:
            if base_currency == target_currency:
                pass
            else:
                insert_currency(base_currency, target_currency)

def get_unique_select_from_data() -> list[str]:
    text = "select DISTINCT from_currency from currency"
    response = cursor.execute(text)
    data = response.fetchall()  # [("USD",), ("EUR",)]
    return [uniq_curr[0] for uniq_curr in data]  # ["USD", "EUR", ...]

def get_to_currency(from_currency) -> list[str]:
    text = f"select to_currency from currency where from_currency = '{from_currency}';"
    response = cursor.execute(text)
    data = response.fetchall()
    return data


def get_exchange_rate(from_currency, to_currency):
    response = (f"https://api.metalpriceapi.com/v1/latest?api_key={api_key}"
                f" base={from_currency}"
                f"&currencies={to_currency}")

    response = requests.get(response)

    data = response.json()
    exchange_rate = data['rates'][to_currency]
    return exchange_rate


@router.message(Command("start"))
async def reply_builder(message: types.Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()

    uniq_curr_from = []
    for curr_from in get_unique_select_from_data():
        builder.add(types.KeyboardButton(text=curr_from))

    builder.adjust(4)
    await message.answer(
        "Виберіть число:",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
    )
    await state.set_state(CurrencyState.first_select)


@router.message(CurrencyState.first_select)
async def second_keyboard(message: types.Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    for to_curr_tuple in get_to_currency(message.text):
        if message.text not in to_curr_tuple:
            print(125)
        to_curr = to_curr_tuple[0]
        from_currency = message.text
        builder.add(types.KeyboardButton(text=f"{from_currency} -> {to_curr}"))

    await message.answer(
        "Choose currency:",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
        )

    await state.set_state(CurrencyState.second_select)


@router.message(CurrencyState.second_select)
async def second_keyboard(message: types.Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    from_currency, to_currency = message.text.split(" -> ")

    await message.answer(f"Currency {message.text} = {get_exchange_rate(from_currency, to_currency)}")

#@router.message(F.text)
#async def reply_builder2(message: types.Message):
 #   builder = ReplyKeyboardBuilder()
#
 #   if "->" in message.text:
  #      from_currency, to_currency = message.text.split(" -> ")

       # await  message.answer(f"Currency {message.text} = {get_exchange_rate(from_currency, to_currency)}")
        #return

    #for to_curr_tuple in get_to_currency(message.text):
     #   to_curr = to_curr_tuple[0]
      #  from_currency = message.text
       # builder.add(types.KeyboardButton(text=f"{from_currency} -> {to_curr}"))
    #await message.answer(
     #   "Choose currency:",
      #  reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
       # )

# DATA_LIST = [
#     {"currency": ("USD", "UAH"), "val": 45.03},
#     {"currency": ("USD", "EUR"), "val": 0.9},
#     {"currency": ("USD", "GBP"), "val": 0.8},
#     {"currency": ("USD", "ZLT"), "val": 5.7},
#     {"currency": ("UAH", "YPI"), "val": 12.0},
# ]


async def main() -> None:
    # ... and all other routers should be attached to Dispatcher
    create_table()
    clear_table()
    add_currency_data()
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

