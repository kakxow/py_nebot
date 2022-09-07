import logging
from types import MethodType

from nechatbot.bot import Bot
from nechatbot.constants import LOGGING_LEVEL
from nechatbot.handler import on_message, on_inline_query

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=LOGGING_LEVEL
)
bot = Bot()
bot.on_message = MethodType(on_message, bot)  # type: ignore
bot.on_inline_query = MethodType(on_inline_query, bot)  # type: ignore
