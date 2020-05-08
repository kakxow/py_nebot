import asyncio
from types import MethodType

from nechatbot.bot import Bot
from nechatbot.constants import BOT_TOKEN
from nechatbot.handler import on_message

bot = Bot(BOT_TOKEN)
bot.on_message = MethodType(on_message, bot)  # type: ignore

asyncio.run(bot.start())
