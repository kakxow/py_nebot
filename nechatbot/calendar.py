from datetime import datetime as dt
import json
import re
from typing import List, Tuple

from .constants import birthday_check_time_tuple
from .trello_main import (
    create_card,
    get_all_cards,
    get_chat_ids_from_board,
    get_card,
    update_card
)


def get_all_birthdays_pretty(chat_id: int) -> str:
    """
    Gets all birthdays and prettifies the result to be sent by the bot. 
    """
    cards = get_all_cards(chat_id, "Calendar")
    all_birthdays = [(json.loads(card.desc), card.due) for card in cards]
    all_birthdays.sort(key=lambda t: t[1])
    text_birthdays = [f"•{r['first_name']} {r['username']}: {r['birthday']}" for r, _ in all_birthdays]
    text = "<b>Nechat birthday calendar</b>\n"
    birthday_table = "\n".join(text_birthdays) or "Nothing to show yet!"
    return text + birthday_table


def update_or_add_birthday(chat_id: int, user: dict, date: str) -> str:
    """
    Updates or creates new user card in calendar Trello list with chat_id in name,
    and returns a keyword for bot's reply.
    """
    card = get_card(chat_id, str(user["id"]), "Calendar")
    if card:
        day, month = day_month_from_date(date)
        due_date = dt(2090, month, day)
        update_card(card, {"birthday": date}, {"due": due_date})
        action = "Updated"
    else:
        create_card(
            chat_id,
            user,
            "Calendar",
            {"birthday": date},
            {"due": convert_date_for_trello(date)}
        )
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
    today = dt.now()
    cards = get_all_cards(chat_id, "Calendar")
    all_birthdays = [(json.loads(card.desc), card.due) for card in cards]
    ids = [int(card["id"]) for card, due in all_birthdays if due[5:10] == f"{today:%m-%d}"]
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
    chat_ids = get_chat_ids_from_board()
    for chat_id in chat_ids:
        ids = get_today_birthdays(int(chat_id))
        print(f"Getting birthday ppl IDs from trello list for {chat_id}")
        if ids:
            chat_members = [await bot.get_chat_member(chat_id, int(id)) for id in ids]
            chat_members_in_chat = [
                chat_member
                for chat_member in chat_members
                if chat_member["status"] != "left"
            ]
            if not chat_members_in_chat:
                continue
            first_names = [
                f'{chat_member.get("user").get("first_name", "")}'
                for chat_member in chat_members_in_chat
                if chat_member
            ]
            usernames = [
                f'@{chat_member.get("user").get("username", "")}'
                for chat_member in chat_members_in_chat
                if chat_member
            ]
            text_usernames = ", ".join(usernames)
            text_first_names = ", ".join(first_names)
            await bot.send_message(chat_id, f"Happy birthday {text_usernames}!")
            await bot.set_chat_title(chat_id, f"Ето не чат с ДР {text_first_names}!")
