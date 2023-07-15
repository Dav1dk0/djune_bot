import os

import logging
import asyncio

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram import html

from aiogram import F

from setting import config

logger = logging.getLogger(__name__)
# Bot token can be obtained via https://t.me/BotFahter


# Dispatcher is a root router
dp = Dispatcher()

# All handlers should be attached to the Router (or Dispatcher)
router = Router()

def user_name(message: Message):
    return message.from_user.full_name



@router.message(Command(commands=["start1"]))
async def command_start_handler1(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    await message.answer(f"Hello, <b>What is your name?</b>")

@router.message(Command(commands=["start"]))
async def start2(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    await message.answer(f"<i>Hello, {message.from_user.full_name}, how i can help you?</i>")

@router.message(Command(commands=["code"]))
async def command_start_handler1(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    f = open('main.py').read()
    await message.answer(f"{f}")

@router.message(Command("fuck"))
async def any_massage(message: Message) -> None:
    await message.reply(f"Hello, {html.bold(html.italic(user_name(message)))}")

@router.message(Command("dice"))
async def any_massage(message: Message) -> None:
    await message.answer_dice()

from aiogram.enums.dice_emoji import DiceEmoji

@router.message(Command("dice2"))
async def any_massage(message: Message) -> None:
    await message.answer_dice(emoji=DiceEmoji.DART)

@router.message(Command("name"))
async def any_massage(message: Message, command: CommandObject) -> None:
    letters = command.args.lower()
    print(letters)
    if 'a' in letters and 'o' in letters:
        await message.answer(f"NY")
    elif 'a' in letters:
        await message.answer(f"LO")
    elif 'o' in letters:
        await message.answer(f"LO")
    else:
        await message.answer(f"IOWA")

@router.message(F.photo)
async def any_massage(message: Message) -> None:
    photo = message.photo[-1]
    await message.answer(f"Your photo, {photo.width}x{photo.height} px)")


async def main() -> None:
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

