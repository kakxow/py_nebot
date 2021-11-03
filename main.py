import asyncio
import logging
from types import MethodType

from nechatbot.bot import Bot
from nechatbot.constants import BOT_TOKEN, LOGGING_LEVEL

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=LOGGING_LEVEL
)
bot = Bot(BOT_TOKEN)
bot.on_message = MethodType(on_message, bot)  # type: ignore

asyncio.run(bot.start())
