import os

import logging
import asyncio

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandObject, Text
from aiogram.types import Message
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


@router.message(Command("start"))
async def reply_builder(message: types.Message):
    builder = ReplyKeyboardBuilder()

    uniq_curr_from = []
    for curr in DATA_LIST:
        curr_from = curr["currency"][0]
        if curr_from not in uniq_curr_from:
            uniq_curr_from.append(curr_from)
            builder.add(types.KeyboardButton(text=curr_from))

    builder.adjust(4)
    await message.answer(
        "Виберіть число:",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
    )

@router.message(F.text)
async def reply_builder2(message: types.Message):
    builder = ReplyKeyboardBuilder()
    uniq_curr_from = []
    for curr in DATA_LIST:
        if curr["currency"][0] == str(message.text):
            curr_from = curr["currency"][1]
            if curr_from not in uniq_curr_from:
                uniq_curr_from.append(curr_from)
                builder.add(types.KeyboardButton(text=curr_from))
                await message.answer(
                "Choose currency:",
                reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
                )
        if curr["currency"][1] == str(message.text):
            await message.answer(f"{curr['val']}")

    builder.adjust(4)





DATA_LIST = [
    {"currency": ("USD", "USD -> UAH"), "val": 45.03},
    {"currency": ("USD", "USD -> EUR"), "val": 0.9},
    {"currency": ("USD", "USD -> GBP"), "val": 0.8},
    {"currency": ("USD", "USD -> ZLT"), "val": 5.7},
    {"currency": ("UAH", "UAH -> YPI"), "val": 12.0},
]


async def main() -> None:
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())