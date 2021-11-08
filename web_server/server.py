import asyncio
import logging
import bottle

from nechatbot.bot import Bot
import settings

if settings.LOGGING_LEVEL == logging.DEBUG:
    bottle.debug(True)

app = bottle.Bottle()
app.logger = logging.getLogger(__name__)


@app.get("/")
def greet():
    asyncio.run(app.bot.send_message("-711229802", "hi!"))
    return "hi"


@app.post(f"/{settings.GITHUB_SECRET}")
def github_webhook():
    push = bottle.request.json
    message = push.get("head_commit", {}).get("message", "")
    sender = push.get("sender", {})
    login = sender.get("login")
    chat_message = f"Hi! New updates in bot repo: \n{message}"
    app.logger.debug(chat_message)
    app.logger.debug(f"{settings.GITHUB_UPDATES_CHAT_ID = }")
    asyncio.run(app.bot.send_message(settings.GITHUB_UPDATES_CHAT_ID, chat_message))
    return message
