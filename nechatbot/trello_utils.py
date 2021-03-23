import json
import threading
from datetime import datetime as dt
from typing import Dict, List, Union

from trello import TrelloClient  # type: ignore

from .constants import (
    CREDIT_FIELD_NAME,
    TRELLO_API_KEY,
    TRELLO_API_SECRET,
    TRELLO_TOKEN,
    TRELLO_NECHAT_LIST_ID,
    TRELLO_NECHAT_CALENDAR_ID
)


client = TrelloClient(
    api_key=TRELLO_API_KEY,
    api_secret=TRELLO_API_SECRET,
    token=TRELLO_TOKEN
)
nechat_list = client.get_list(TRELLO_NECHAT_LIST_ID)
board = client.get_board()
board.get_lists()
nechat_calendar = client.get_list(TRELLO_NECHAT_CALENDAR_ID)


class NameNotFound(BaseException):
    pass


def get_today_birthdays() -> List[str]:
    today = dt.now()
    today = dt(2020,7,25)
    all_records = get_all_birthdays()
    ids = [card["id"] for card, due in all_records if due[5:10] == f"{today:%m-%d}"]
    return ids


def convert_date_for_trello(date: str) -> str:
    day, month = date.split(".")
    return f"2090-{month}-{day}"


def add_birthday_card(user: dict, date: str) -> None:
    # Check for unique.
    card_data = {
        "id": str(user["id"]),
        "first_name": user["first_name"],
        "last_name": user.get("last_name", ""),
        "username": user.get("username", ""),
        "birthday": date
    }
    card_name = f"{user['id']} {user['first_name']}"
    nechat_calendar.add_card(
        name=card_name,
        desc=json.dumps(card_data),
        due=convert_date_for_trello(date)
    )
    print(f"Created new record {user['first_name']} with birthday {date}")


def get_all_birthdays() -> List[Dict[str, str]]:
    all_records = [(json.loads(card.desc), card.due) for card in nechat_calendar.list_cards()]
    return all_records


def get_all_birthdays_pretty():
    all_records = get_all_birthdays()
    all_records.sort(key=lambda t: t[1])
    text_records = [f"{r['first_name']} {r['username']}: {r['birthday']}" for r, _ in all_records]
    text = "Nechat birthday calendar\n"
    record_table = "\n".join(text_records) or "Nothing to show yet!"
    return text + record_table


def get_all_scores() -> List[Dict[str, Union[str, int]]]:
    all_records = [json.loads(card.desc) for card in nechat_list.list_cards_iter() if card.desc.startswith("{")]
    all_records.sort(key=lambda c: c[CREDIT_FIELD_NAME], reverse=True)
    return all_records


def get_all_scores_pretty() -> str:
    scores = get_all_scores()
    text_scores = [f"{record['first_name']} {record['username']}: {record[CREDIT_FIELD_NAME]}" for record in scores]
    text = "Nechat Social Credit System scores:\n"
    score_table = "\n".join(text_scores) or "Nothing to show yet!"
    return text + score_table


def add_record(user: dict, score: int = 0) -> None:
    card_data = {
        "id": str(user["id"]),
        "first_name": user["first_name"],
        "last_name": user.get("last_name", ""),
        "username": user.get("username", ""),
        CREDIT_FIELD_NAME: score
    }
    card_name = f"{user['id']} {user['first_name']}"
    nechat_list.add_card(name=card_name, desc=json.dumps(card_data))
    print(f"Created new record {user['first_name']} with score {score}")


def check_id(card, id: Union[str, int]) -> bool:
    try:
        id_from_card, _ = card.name.split()
    except ValueError:
        return False
    return id_from_card == str(id)


def add_credits(user: dict, credits: int) -> None:
    search_results = [card for card in nechat_list.list_cards() if check_id(card, user["id"])]
    if not search_results:
        raise NameNotFound
    target_card = search_results[0]
    card_data = json.loads(target_card.desc)
    card_data[CREDIT_FIELD_NAME] += credits
    target_card.set_description(json.dumps(card_data))
    print(f"Record {card_data['first_name']} has score of {card_data[CREDIT_FIELD_NAME]} now")


def _add_credits_or_record(user: dict, credits: int) -> None:
    try:
        add_credits(user, credits)
    except NameNotFound:
        add_record(user, credits)


def add_credits_or_record(user: dict, credits: int):
    t = threading.Thread(target=_add_credits_or_record, args=(user, credits))
    t.start()
    print("Thread started")
