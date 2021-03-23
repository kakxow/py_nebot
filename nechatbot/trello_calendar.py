from datetime import datetime as dt
import json

from .trello_main import get_list


def get_today_birthdays(chat_id: int):
    today = dt.now()
    today = dt(2020, 7, 25)
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
