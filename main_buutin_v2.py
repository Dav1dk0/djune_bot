import os

import logging
import asyncio

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, URLInputFile
from dotenv import load_dotenv
from aiogram import html
from aiogram.filters import Text
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import random

from setting import config

logger = logging.getLogger(__name__)
# Bot token can be obtained via https://t.me/BotFahter

load_dotenv()

# Dispatcher is a root router
dp = Dispatcher()

# All handlers should be attached to the Router (or Dispatcher)
router = Router()


@router.message(Command("random_image"))
async def get_random_image(message: types.Message, command: CommandObject) -> None:
    if len(command.args) > 0:
        print(int(command.args.split()[0]))
        comm = command.args.split()
        rand_width = comm[0]
        rand_heinght = comm[1]
    else:
        rand_width = random.randint(32, 1920)
        rand_heinght = random.randint(32, 1080)

    image_from_url = URLInputFile(f"https://random.imagecdn.app/{rand_width}/{rand_heinght}")
    await message.answer_photo(
        image_from_url,
        caption=f"Image {rand_width}x{rand_heinght} px"
    )


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
