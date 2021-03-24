import json
import threading
from typing import Dict, List, Union

from .constants import CREDIT_FIELD_NAME
from .trello_main import get_list, NameNotFound


def get_all_scores(chat_id: int) -> List[Dict[str, Union[str, int]]]:
    score_list = get_list(chat_id, "Credit")
    all_records = [json.loads(card.desc) for card in score_list.list_cards()]
    all_records.sort(key=lambda c: c[CREDIT_FIELD_NAME], reverse=True)
    return all_records


def get_all_scores_pretty(chat_id: int) -> str:
    scores = get_all_scores(chat_id)
    text_scores = [f"•{record['first_name']} {record['username']}: {record[CREDIT_FIELD_NAME]}" for record in scores]
    text = "<b>Nechat Social Credit System scores</b>\n"
    score_table = "\n".join(text_scores) or "Nothing to show yet!"
    return text + score_table


def add_record(chat_id: int, user: dict, score: int = 0) -> None:
    score_list = get_list(chat_id, "Credit")
    card_data = {
        "id": str(user["id"]),
        "first_name": user["first_name"],
        "last_name": user.get("last_name", ""),
        "username": user.get("username", ""),
        CREDIT_FIELD_NAME: score
    }
    card_name = f"{user['id']} {user['first_name']}"
    score_list.add_card(name=card_name, desc=json.dumps(card_data))
    print(f"Created new record {user['first_name']} with score {score}")


def check_id(card, id: Union[str, int]) -> bool:
    try:
        id_from_card, *_ = card.name.split()
    except ValueError:
        return False
    return id_from_card == str(id)


def add_credits(chat_id: int, user: dict, credits: int) -> None:
    score_list = get_list(chat_id, "Credit")
    search_results = [card for card in score_list.list_cards() if check_id(card, user["id"])]
    if not search_results:
        raise NameNotFound
    target_card = search_results[0]
    card_data = json.loads(target_card.desc)
    card_data[CREDIT_FIELD_NAME] += credits
    target_card.set_description(json.dumps(card_data))
    print(f"Record {card_data['first_name']} has score of {card_data[CREDIT_FIELD_NAME]} now")


def _add_credits_or_record(chat_id: int, user: dict, credits: int) -> None:
    try:
        add_credits(chat_id, user, credits)
    except NameNotFound:
        add_record(chat_id, user, credits)


def add_credits_or_record(chat_id: int, user: dict, credits: int):
    t = threading.Thread(target=_add_credits_or_record, args=(chat_id, user, credits))
    t.start()
    print("Thread started")
