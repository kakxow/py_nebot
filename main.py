import asyncio
import logging

from nechatbot.bot import Bot
from nechatbot.constants import BOT_TOKEN
from nechatbot.handler import on_message, on_inline_query
from settings import LOGGING_LEVEL
from web_server.server import app


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=LOGGING_LEVEL
)

bot = Bot(BOT_TOKEN, on_message, on_inline_query)
app.bot = bot
asyncio.ensure_future(bot.start())
