import asyncio

from asgi_tools import App, ResponseError

from main import bot
from nechatbot.constants import SECURITY_KEY

app = App()


@app.route("/", methods=["POST"])
async def get_update(request):
    print(request)
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token", "") != SECURITY_KEY:
        return ResponseError(status_code=401)
    update = await request.json()
    asyncio.ensure_future(bot.process_update(update))
    return 200, "OK"
