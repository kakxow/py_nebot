from datetime import datetime as dt
import json

from .constants import birthday_check_time_tuple
from .trello_main import get_chat_ids_from_board, get_list


def get_today_birthdays(chat_id: int):
    today = dt.now()
    all_records = get_all_birthdays(chat_id)
    ids = [card["id"] for card, due in all_records if due[5:10] == f"{today:%m-%d}"]
    return ids


def convert_date_for_trello(date: str) -> str:
    day, month = date.split(".")
    return f"2090-{month}-{day}"


def get_card_for_user(chat_id: int, user_id: str):
    calendar_list = get_list(chat_id, "Calendar")
    eglible_cards = [c for c in calendar_list.list_cards() if c.name.split()[0] == user_id]
    if eglible_cards:
        return eglible_cards[0]
    else:
        return None


def update_or_add_birthday_card(chat_id: int, user: dict, date: str) -> None:
    card = get_card_for_user(chat_id, str(user["id"]))
    if card:
        card_data = json.loads(card.desc)
        card_data["birthday"] = date
        card.set_description(json.dumps(card_data))
        day, month = date.split(".")
        card.set_due(dt(2090, int(month), int(day)))
        action = "Updated a"
    else:
        calendar_list = get_list(chat_id, "Calendar")
        card_data = {
            "id": str(user["id"]),
            "first_name": user["first_name"],
            "last_name": user.get("last_name", ""),
            "username": user.get("username", ""),
            "birthday": date
        }
        card_name = f"{user['id']} {user['first_name']}"
        calendar_list.add_card(
            name=card_name,
            desc=json.dumps(card_data),
            due=convert_date_for_trello(date)
        )
        action = "Created new"
    print(f"{action} record {user['first_name']} with birthday {date}")


def get_all_birthdays(chat_id: int):
    calendar_list = get_list(chat_id, "Calendar")
    all_records = [(json.loads(card.desc), card.due) for card in calendar_list.list_cards()]
    return all_records


def get_all_birthdays_pretty(chat_id: int):
    all_records = get_all_birthdays(chat_id)
    all_records.sort(key=lambda t: t[1])
    text_records = [f"•{r['first_name']} {r['username']}: {r['birthday']}" for r, _ in all_records]
    text = "<b>Nechat birthday calendar</b>\n"
    record_table = "\n".join(text_records) or "Nothing to show yet!"
    return text + record_table


async def check_birthdays(bot):
    now = dt.now()
    if (now.hour, now.minute, now.second) == birthday_check_time_tuple:
        print("Checking birthdays")
        await congrats_today_birthdays(bot)


async def congrats_today_birthdays(bot):
    print("Getting chat_ids from trello board")
    chat_ids = get_chat_ids_from_board()
    for chat_id in chat_ids:
        ids = get_today_birthdays(chat_id)
        print(f"Getting birthday ppl IDs from trello list for {chat_id}")
        if ids:
            chat_members = [await bot.get_chat_member(chat_id, int(id)) for id in ids]
            first_names = [f'{chat_member.get("user").get("first_name", "")}' for chat_member in chat_members if chat_member]
            usernames = [f'@{chat_member.get("user").get("username", "")}' for chat_member in chat_members if chat_member]
            text_usernames = ", ".join(usernames)
            text_first_names = ", ".join(first_names)
            await bot.send_message(chat_id, f"Happy birthday {text_usernames}!")
            await bot.set_chat_title(chat_id, f"Ето не чат с ДР {text_first_names}!")
