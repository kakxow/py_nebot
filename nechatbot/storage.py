import json
from typing import Any, Callable

import httpx

from .constants import JSON_SECURITY_KEY, BIN_URL
from .nechat_types import Chat, encode_chat, decode_chats, make_user, User


headers = {"Security-key": JSON_SECURITY_KEY}


def get_chats() -> dict[int, Chat]:
    return fetch_storage("chats", decode_chats)


def fetch_storage(term: str, json_decoder: Callable = json.JSONDecoder) -> dict:
    response = httpx.get(BIN_URL, headers=headers)
    response.raise_for_status()
    match term:
        case "chats":
            return response.json(object_hook=json_decoder)
        case "tags":
            return response.json(object_hook=json_decoder)
    return {}


def update_storage(
    term: str, data: dict, json_encoder: Callable = json.JSONEncoder
) -> None:
    patch_command = [
        {
            "op": "replace",
            "path": f"/{term}",
            "value": json.dumps(data, default=json_encoder),
        }
    ]
    response = httpx.patch(BIN_URL, json=patch_command)
    response.raise_for_status()


def update_chats(chats: dict[int, Chat]) -> None:
    data = json.dumps(chats, default=encode_chat)
    result = httpx.put(BIN_URL, data=data, headers=headers)
    result.raise_for_status()


def update_user(chat_id: int, user: dict, **updates: Any) -> User:
    """user: dict is Telegram Bot API User type."""
    chats = get_chats()
    user_id = user["id"]
    if chat_id in chats:
        if user_id in chats[chat_id].users:
            chats[chat_id].users[user_id].update(updates)
        else:
            new_user = make_user(user).update(updates)
            chats[chat_id].users[user_id] = new_user
    else:
        new_user = make_user(user).update(updates)
        chats[chat_id] = Chat(chat_id, users={user_id: new_user})
    update_chats(chats)
    return chats[chat_id].users[user_id]


def remove_user(chat_id: int, user_id: int) -> None:
    chats = get_chats()
    if chat_id in chats:
        chats[chat_id].users.pop(user_id, None)
    update_chats(chats)
