from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class User:
    user_id: int
    first_name: str
    last_name: str = ""
    username: str = ""
    birthday: str = ""
    credit: int = 0
    location: str = ""

    def update(self, updates: dict) -> User:
        updates = {k: v for k, v in updates.items() if k in User.__annotations__.keys()}
        self.__dict__.update(updates)
        return self


@dataclass
class Chat:
    chat_id: int
    users: dict[int, User] = field(default_factory=dict)


def encode_chat(chat: Chat) -> dict:
    return chat.__dict__


def decode_chats(dct: dict) -> Chat | User | dict[int, Chat] | dict[int, User]:
    if "user_id" in dct:
        return User(**dct)
    if "chat_id" in dct:
        return Chat(**dct)
    return dct


def make_user(d: dict) -> User:
    user_params = User.__annotations__.keys()
    user_dict = {}
    if "user_id" not in d and "id" in d:
        d["user_id"] = d["id"]
    user_dict = {k: v for k, v in d.items() if k in user_params}
    return User(**user_dict)
