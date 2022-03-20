from datetime import datetime as dt
import json
import re
from typing import List, Tuple

from .constants import birthday_check_time_tuple
from . import storage_utils


def get_all_birthdays_pretty(chat_id: int) -> str:
    """
    Gets all birthdays and prettifies the result to be sent by the bot.
    """
    storage = storage_utils.Storage()
    users = storage.get_users_for_chat(chat_id)
    users.sort(key=lambda user: user["birthday"])
    text_birthdays = [
        f"•{user['first_name']} {user['username']}: {user['birthday']}"
        for user in users
    ]
    text = "<b>Nechat birthday calendar</b>\n"
    birthday_table = "\n".join(text_birthdays) or "Nothing to show yet!"
    return text + birthday_table


def update_or_add_birthday(chat_id: int, user: dict, date: str) -> str:
    """
    Updates or creates new user card in calendar Trello list with chat_id in name,
    and returns a keyword for bot's reply.
    """
    storage = storage_utils.Storage()
    user_id = user["id"]
    new_user = storage.get_user(user_id)
    day, month = day_month_from_date(date)
    new_date = f"{month}.{day}"
    if new_user:
        new_user["birthday"] = new_date
        storage.update_user(user_id, new_user)
        action = "Updated"
    else:
        new_user = storage_utils.create_user_from_tg_user(**user, birthday=new_date)
        storage.update_user(user_id, new_user)
        action = "Created"
    return action


def day_month_from_date(date: str) -> Tuple[int, int]:
    """
    Returns a tuple of day and month integers from a string with date in format
    dd.mm, where "." may be any non-digit character.
    """
    day, month, *_ = [int(el) for el in re.split(r"\D", date)]
    return day, month


def convert_date_for_trello(date: str) -> str:
    """
    Converts a string with date in format dd.mm (where "." may be any non-digit
    character), to a date string in format 2090-m-d
    """
    day, month = day_month_from_date(date)
    return f"2090-{month}-{day}"


def get_today_birthdays(chat_id: int) -> List[int]:
    """
    From a calendar Trello list with chat_id in name, returns a list of user_ids,
    who have a birthday today.
    """
    storage = storage_utils.Storage()
    today = dt.now()
    users = storage.get_users_for_chat(chat_id)
    ids = [user["user_id"] for user in users if user["birthday"] == f"{today:%m.%d}"]
    return ids


async def check_birthdays(bot) -> None:
    """
    Checks if current time (hour, minute, second) is equal to the built-in
    birthday_check_time_tuple, and if it is fires congratulations in all chats,
    present in the Trello board.
    """
    now = dt.now()
    now_time_tuple = (now.hour, now.minute, now.second)
    if now_time_tuple == birthday_check_time_tuple:
        print("Checking birthdays")
        await congrats_today_birthdays(bot)


async def congrats_today_birthdays(bot) -> None:
    """
    Fires birthday congratulations mentioning usernames in chat and changing
    chat titles where possible.
    """
    print("Getting chat_ids from trello board")
    storage = storage_utils.Storage()
    chat_ids = storage.get_chat_ids()
    for chat_id in chat_ids:
        ids = get_today_birthdays(int(chat_id))
        print(f"Getting birthday ppl IDs from trello list for {chat_id}")
        if ids:
            chat_members = [await bot.get_chat_member(chat_id, int(id)) for id in ids]
            first_names = [
                f'{chat_member.get("user").get("first_name", "")}'
                for chat_member in chat_members
                if chat_member
            ]
            usernames = [
                f'@{chat_member.get("user").get("username", "")}'
                for chat_member in chat_members
                if chat_member
            ]
            text_usernames = ", ".join(usernames)
            text_first_names = ", ".join(first_names)
            await bot.send_message(chat_id, f"Happy birthday {text_usernames}!")
            await bot.set_chat_title(chat_id, f"Ето не чат с ДР {text_first_names}!")
