import asyncio

from nechatbot.bot import Bot

liza_id = 177121435
nechat_id = -1001365498540
text = f'<a href="tg://user?id={liza_id}">liza_zhdan</a> НАВЫКИ ДБТ!!!!!'

bot = Bot()
asyncio.get_event_loop().run_until_complete(bot.send_message(nechat_id, text))
