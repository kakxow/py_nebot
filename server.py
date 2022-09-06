import asyncio

from asgi_tools import App, ResponseError, Request

from main import bot
from nechatbot.constants import SECURITY_KEY

app = App()


@app.route("/", methods=["POST"])
async def get_update(request: Request) -> tuple[int, str] | ResponseError:
    print(request)
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token", "") != SECURITY_KEY:
        return ResponseError(status_code=401)
    update = await request.json()
    asyncio.ensure_future(bot.dispatch_update(update))
    return 200, "OK"
