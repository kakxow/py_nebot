import asyncio
import logging
import threading

from nechatbot.bot import Bot
from nechatbot.constants import BOT_TOKEN
from nechatbot.handler import on_message, on_inline_query
from settings import LOGGING_LEVEL
from web_server.server import app


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=LOGGING_LEVEL
)
bot = Bot(BOT_TOKEN, on_message, on_inline_query)


def start():
    asyncio.run(bot.start())


# t = threading.Thread(target=start, daemon=True)
# t.start()
bot.start_threaded()


# app.config["bot"] = bot
app.bot = bot
# app = app_factory(bot)
app.run(host="localhost", port="80")
