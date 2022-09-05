import asyncio

from flask import Flask, request, abort

from main import bot
from nechatbot.constants import SECURITY_KEY


app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_update():
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token", "") != SECURITY_KEY:
        return abort(401)
    update = request.json
    asyncio.ensure_future(bot.process_update(update))
    return "OK", 200
