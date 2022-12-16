import asyncio

from nechatbot import calendar
from nechatbot.bot import Bot


bot = Bot()
asyncio.run(calendar.congrats_today_birthdays(bot))
