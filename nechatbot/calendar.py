from datetime import datetime as dt
from itertools import groupby

from .bot import Bot

from .db import Session, update_user
from .nechat_db_types import User


def dm_to_md(date: str) -> str:
    """Converts date in format day.month to month.day format, for sorting."""
    day, month = date.split(".")
    return ".".join([month, day])


def get_all_birthdays_pretty(chat_id: int) -> str:
    """
    Gets all birthdays and prettifies the result to be sent by the bot.
    """
    with Session() as session:
        users_with_bdays = (
            session.query(User)
            .filter(
                User.chat == chat_id,
                User.birthday != None,  # "is not None" won't work cuz magic.
            )
            .all()
        )
        users_with_bdays.sort(key=lambda u: dm_to_md(u.birthday))
        text_birthdays = [
            f"•{user.first_name} {user.username}: {user.birthday}"
            for user in users_with_bdays
        ]
        text = "<b>Nechat birthday calendar</b>\n"
        birthday_table = "\n".join(text_birthdays) or "Nothing to show yet!"
        return text + birthday_table


def update_or_add_birthday(chat_id: int, user: dict, date: str) -> None:
    update_user(chat_id, user, {"birthday": date})


async def congrats_today_birthdays(bot: Bot) -> None:
    """
    Fires birthday congratulations mentioning usernames in chat and changing
    chat titles where possible.
    """

    with Session() as session:
        today = f"{dt.now():%d.%m}"
        result = (
            session.query(User.chat, User.id)
            .filter(User.birthday == today)
            .order_by(User.chat)
            .all()
        )
        for chat_id, group in groupby(result, lambda el: el[0]):
            chat_members: list[dict] = []
            for _, user_id in group:
                chat_member = await bot.get_chat_member(chat_id, user_id)
                if chat_member.get("status", "left") != "left":
                    chat_members.append(chat_member)
            if not chat_members:
                continue

            first_names: list[str] = []
            usernames: list[str] = []
            for chat_member in chat_members:
                first_name = chat_member["user"]["first_name"]
                mention = f'<a href="tg://user?id={chat_member["user"]["id"]}">{first_name}</a>'
                first_names.append(first_name)
                usernames.append(mention)

            mentions = ", ".join(usernames)
            title_names = ", ".join(first_names)
            await bot.send_message(chat_id, f"Happy birthday {mentions}!")
            await bot.set_chat_title(chat_id, f"Ето не чат с ДР {title_names}!")
