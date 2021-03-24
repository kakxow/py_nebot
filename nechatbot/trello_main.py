from functools import lru_cache
import json
from operator import attrgetter
from typing import List, Optional, Set

import trello  # type: ignore

from .constants import (
    TRELLO_API_KEY,
    TRELLO_API_SECRET,
    TRELLO_TOKEN,
    TRELLO_NECHAT_BOARD
)


def get_client():
    """
    Yields a trello client.
    """
    client = trello.TrelloClient(
        api_key=TRELLO_API_KEY,
        api_secret=TRELLO_API_SECRET,
        token=TRELLO_TOKEN
    )
    while 1:
        yield client


@lru_cache
def get_list(chat_id: int, prefix: str) -> trello.List:
    """
    Returns a trello list with the name "prefix chat_id". Cached!
    """
    list_name = f"{prefix} {chat_id}"
    client = next(get_client())
    board = client.get_board(TRELLO_NECHAT_BOARD)
    lists = board.list_lists()
    target_list = [el for el in lists if el.name == list_name]
    if not target_list:
        target_list = [board.add_list(list_name)]
    return target_list[0]


def get_chat_ids_from_board() -> Set[str]:
    client = next(get_client())
    board = client.get_board(TRELLO_NECHAT_BOARD)
    lists = board.list_lists()
    chat_ids = {el.name.split()[1] for el in lists}
    return chat_ids


def create_card(
    chat_id: int,
    user: dict,
    prefix: str,
    desc_data: dict,
    constructor_arguments: dict = None
) -> trello.Card:
    """
    Creates and returns a new trello.Card from a template with given description
    and other properties (optional).
    """
    if not constructor_arguments:
        constructor_arguments = {}
    card_name = f"{user['id']} {user['first_name']}"
    card_data = {
        "id": str(user["id"]),
        "first_name": user["first_name"],
        "last_name": user.get("last_name", ""),
        "username": user.get("username", ""),
    }
    card_data.update(desc_data)
    
    trello_list = get_list(chat_id, prefix)
    new_card = trello_list.add_card(
        name=card_name,
        desc=json.dumps(card_data),
        **constructor_arguments,
    )
    return new_card


def update_card(card: trello.Card, desc_changes: dict, card_changes: dict) -> trello.Card:
    """
    Updates given card's description and other properties.
    """
    card_data: dict = json.loads(card.desc)
    card_data.update(desc_changes)
    card.set_description(json.dumps(card_data))
    
    for property, value in card_changes.items():
        setter = attrgetter(f"set_{property}")(card)
        setter(value)
    return card


def get_card(chat_id: int, user_id: str, prefix: str) -> Optional[trello.Card]:
    """
    Returns a trello.Card or None for a given user_id from a calendar Trello list
    with chat_id in name.
    """
    trello_list = get_list(chat_id, prefix)
    eglible_cards = [c for c in trello_list.list_cards() if c.name.split()[0] == user_id]
    if eglible_cards:
        return eglible_cards[0]
    else:
        return None


def get_all_cards(chat_id: int, prefix: str) -> List[trello.Card]:
    trello_list = get_list(chat_id, prefix)
    all_records = [card for card in trello_list.list_cards()]
    return all_records
