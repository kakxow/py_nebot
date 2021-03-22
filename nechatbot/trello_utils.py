import json
import threading

from trello import TrelloClient  # type: ignore

from .constants import CREDIT_FIELD_NAME, TRELLO_API_KEY, TRELLO_API_SECRET, TRELLO_TOKEN, TRELLO_NECHAT_LIST_ID


client = TrelloClient(
    api_key=TRELLO_API_KEY,
    api_secret=TRELLO_API_SECRET,
    token=TRELLO_TOKEN
)


class NameNotFound(BaseException):
    pass


def get_all_scores() -> list:
    nechat_list = client.get_list(TRELLO_NECHAT_LIST_ID)
    all_records = [json.loads(card.desc) for card in nechat_list.list_cards_iter() if card.desc.startswith("{")]
    all_records.sort(key=lambda c: c[CREDIT_FIELD_NAME])
    return all_records


def get_all_scores_pretty() -> str:
    scores = get_all_scores()
    text_scores = [f"{record['first_name']} {record['username']} - {record[CREDIT_FIELD_NAME]}" for record in scores]
    return "\n".join(text_scores)


def add_record(user: dict, score: int = 0) -> None:
    card_data = {
        "id": str(user["id"]),
        "first_name": user["first_name"],
        "last_name": user.get("last_name", ""),
        "username": user.get("username", ""),
        CREDIT_FIELD_NAME: score
    }
    nechat_list = client.get_list(TRELLO_NECHAT_LIST_ID)
    nechat_list.add_card(name=str(user["id"]), desc=json.dumps(card_data))
    print(f"Created new record {user['first_name']} with score {score}")


def check_id(card, id: str) -> bool:
    try:
        card_data = json.loads(card.desc)
        assert isinstance(card_data, dict)
    except Exception:
        return False
    return card_data["id"] == id


def add_credits(user: dict, credits: int) -> None:
    nechat_list = client.get_list(TRELLO_NECHAT_LIST_ID)
    search_results = [card for card in nechat_list.list_cards() if check_id(card, str(user["id"]))]
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
