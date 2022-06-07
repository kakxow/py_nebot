from __future__ import annotations
from datetime import datetime as dt

from .nechat_types import Chat
from .bot import Bot
from . import storage
from .predicates import is_date


def dm_to_md(date: str) -> str:
    """Converts date in format day.month to month.day format, for sorting."""
    day, month = date.split(".")
    return ".".join([month, day])


def get_all_birthdays_pretty(chat_id: str) -> str:
    """
    Gets all birthdays and prettifies the result to be sent by the bot.
    """
    chats = storage.get_chats()
    chat = chats.get(chat_id, Chat(chat_id))
    all_birthdays = [user for user in chat.users.values() if user.birthday]
    all_birthdays.sort(key=lambda u: dm_to_md(u.birthday))
    text_birthdays = [
        f"•{user.first_name} {user.username}: {user.birthday}" for user in all_birthdays
    ]
    text = "<b>Nechat birthday calendar</b>\n"
    birthday_table = "\n".join(text_birthdays) or "Nothing to show yet!"
    return text + birthday_table


def update_or_add_birthday(chat_id: str, user: dict, date: str) -> None:
    storage.update_user(chat_id, user, birthday=date)


def get_today_birthdays(chat_id: str, date: str = "") -> list[str]:
    """
    Returns a list of user_ids who have a birthday today.
    """
    today = date if is_date(date) else f"{dt.now():%d.%m}"
    chats = storage.get_chats()
    chat = chats.get(chat_id, Chat(chat_id))
    todays_namesakes = [
        user.user_id for user in chat.users.values() if user.birthday == today
    ]
    return todays_namesakes


async def congrats_today_birthdays(bot: Bot) -> None:
    """
    Fires birthday congratulations mentioning usernames in chat and changing
    chat titles where possible.
    """
    chats = storage.get_chats()
    for chat_id in chats:
        ids = get_today_birthdays(chat_id)
        print(f"Getting namesakes' IDs for {chat_id}")
        if ids:
            chat_members = [await bot.get_chat_member(chat_id, int(id)) for id in ids]
            chat_members = list(filter(None, chat_members))
            chat_members_in_chat = [
                chat_member
                for chat_member in chat_members
                if chat_member.get("status", "") != "left"
            ]
            if not chat_members_in_chat:
                continue
            first_names = [
                f'{chat_member["user"].get("first_name", "")}'
                for chat_member in chat_members_in_chat
                if chat_member
            ]
            usernames = [
                f'@{chat_member["user"].get("username", "")}'
                for chat_member in chat_members_in_chat
                if chat_member
            ]
            text_usernames = ", ".join(usernames)
            text_first_names = ", ".join(first_names)
            await bot.send_message(chat_id, f"Happy birthday {text_usernames}!")
            await bot.set_chat_title(chat_id, f"Ето не чат с ДР {text_first_names}!")
