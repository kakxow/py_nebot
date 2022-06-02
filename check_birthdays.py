import asyncio

from nechatbot import calendar
from nechatbot.bot import Bot
from nechatbot.constants import BOT_TOKEN


bot = Bot(BOT_TOKEN)
asyncio.run(calendar.congrats_today_birthdays(bot))
