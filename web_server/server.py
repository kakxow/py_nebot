import logging

import asgi_tools

import settings


app = asgi_tools.app.App(logger=logging.getLogger(__name__))


@app.route("/")
async def greet(request):
    if app.logger.level == logging.DEBUG:
        await app.bot.send_message("-711229802", "hi!")
    return asgi_tools.response.Response("Hi", 200)


@app.route(f"/{settings.GITHUB_SECRET}", methods=["POST"])
async def github_webhook(request: asgi_tools.request.Request):
    push = await request.json()
    if not isinstance(push, dict):
        return
    ref = push.get("ref", "")
    if not (ref.endswith("master") or ref.endswith("main")):
        app.logger.debug("Push to %s", ref)
        return asgi_tools.response.Response("OK", 200)
    message = push.get("head_commit", {}).get("message", "")
    chat_message = f"Hi! New updates in bot repo: \n{message}"
    app.logger.debug(chat_message)
    res = await app.bot.send_message(settings.GITHUB_UPDATES_CHAT_ID, chat_message)
    if res:
        return asgi_tools.response.Response("OK", 200)
    return asgi_tools.response.ResponseError("Message not sent.", 500)
