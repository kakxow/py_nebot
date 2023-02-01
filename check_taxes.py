import asyncio

from nechatbot.bot import Bot
from nechatbot.location import get_people_from_location


nechat_id = -1001365498540


def tagline_tbilisi(chat_id: int) -> str:
    template = '<a href="tg://user?id={}">{}</a>'
    users_from_tbilisi = get_people_from_location(chat_id, "tbl")
    return ", ".join(
        [
            template.format(user.id, user.username or user.first_name)
            for user in users_from_tbilisi
        ]
    )


bot = Bot()
msg = "ПЛОТИ НОЛОГИ " + tagline_tbilisi(nechat_id)
asyncio.get_event_loop().run_until_complete(bot.send_message(nechat_id, msg))
