from functools import lru_cache

from trello import TrelloClient  # type: ignore

from .constants import (
    TRELLO_API_KEY,
    TRELLO_API_SECRET,
    TRELLO_TOKEN,
    TRELLO_NECHAT_BOARD
)


def get_client():
    client = TrelloClient(
        api_key=TRELLO_API_KEY,
        api_secret=TRELLO_API_SECRET,
        token=TRELLO_TOKEN
    )
    while 1:
        yield client


@lru_cache
def get_list(chat_id: int, prefix: str):
    list_name = f"{prefix} {chat_id}"
    client = next(get_client())
    board = client.get_board(TRELLO_NECHAT_BOARD)
    lists = board.list_lists()
    target_list = [el for el in lists if el.name == list_name]
    if not target_list:
        target_list = [board.add_list(list_name)]
    return target_list[0]


def get_chat_ids_from_board():
    client = next(get_client())
    board = client.get_board(TRELLO_NECHAT_BOARD)
    lists = board.list_lists()
    chat_ids = {el.name.split()[1] for el in lists}
    return chat_ids


class NameNotFound(BaseException):
    pass
