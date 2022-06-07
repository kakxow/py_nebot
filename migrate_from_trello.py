from __future__ import annotations
from collections import defaultdict
import json
import trello

from nechatbot import storage, trello_main

from nechatbot.constants import TRELLO_NECHAT_BOARD
from nechatbot.nechat_types import Chat, make_user


def fetch_all_cards() -> dict[str, list[trello.Card]]:
    client = next(trello_main.get_client())
    board = client.get_board(TRELLO_NECHAT_BOARD)
    lists = board.list_lists()
    all_data = defaultdict(list)
    for trello_list in lists:
        cards = trello_list.list_cards()
        if not cards:
            continue
        _, chat_id = trello_list.name.split()
        all_data[chat_id].extend(cards)
    return all_data


def make_new(all_cards: dict[str, list[trello.Card]]) -> dict[str, Chat]:
    chats: dict[str, Chat] = {}
    for chat_id, cards in all_cards.items():
        users_raw: dict[str, dict] = defaultdict(dict)
        for card in cards:
            user_id, *_ = card.name.split()
            user_data = json.loads(card.desc)
            users_raw[user_id].update(user_data)
        users = {id: make_user(user) for id, user in users_raw.items()}
        chats[chat_id] = Chat(chat_id, users)
    return chats


if __name__ == "__main__":
    all_data = fetch_all_cards()
    print("all_data_fetched")
    chats = make_new(all_data)
    storage.update_chats(chats)
