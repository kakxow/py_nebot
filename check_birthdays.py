import asyncio

from nechatbot import calendar
from nechatbot.bot import Bot


bot = Bot()
asyncio.get_event_loop().run_until_complete(calendar.congrats_today_birthdays(bot))
