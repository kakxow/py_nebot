import asyncio

import bottle


def github_webhook():
    pass


@bottle.get("/")
def greet():
    bot = bottle.default_app().config["bot"]
    asyncio.run(bot.send_message("-711229802", "hi!"))
    return "hi"
