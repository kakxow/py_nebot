import asyncio

from asgi_tools import App, ResponseError, Request

from main import bot
from nechatbot.calendar import congrats_today_birthdays
from nechatbot.constants import SECURITY_KEY, POLL

app = App()

if POLL:
    asyncio.get_event_loop().run_until_complete(bot.start())


@app.route("/", methods=["POST"])
async def get_update(request: Request) -> tuple[int, str] | ResponseError:
    print(request)
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token", "") != SECURITY_KEY:
        return ResponseError(status_code=401)
    update = await request.json()
    asyncio.ensure_future(bot.dispatch_update(update))
    return 200, "OK"


@app.route("/health_check", methods=["GET"])
async def health_check(_request: Request) -> tuple[int, str]:
    return 200, "OK"


@app.route("/check_birthdays", methods=["GET"])
async def check_birthdays(request: Request) -> tuple[int, str] | ResponseError:
    if request.headers.get("Security-key") == SECURITY_KEY:
        await congrats_today_birthdays(bot)
        return 200, "OK"
    return ResponseError(status_code=401)
