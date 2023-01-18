import asyncio

from nechatbot.bot import Bot


bot = Bot()
asyncio.get_event_loop().run_until_complete(
    bot.send_message(-1001365498540, "вы все таблетки выпили? а? а?")
)
