import asyncio

from asgi_tools import App


from main import bot
from nechatbot.constants import SECURITY_KEY

app = App()


@app.route("/", methods=["POST"])
def get_update(request):
    print(request)
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token", "") != SECURITY_KEY:
        return 401
    update = request.json
    asyncio.ensure_future(bot.process_update(update))
    return "OK", 200


# run(app, host="localhost", port=80)
