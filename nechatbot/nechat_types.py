from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Tag:
    name: str
    description: str
    tags: list[str]


@dataclass
class User:
    user_id: int
    first_name: str
    last_name: str = ""
    username: str = ""
    birthday: str = ""
    credit: int = 0
    location: str = ""
    tags: list[str] = []

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
        dct["user_id"] = int(dct["user_id"])
        return User(**dct)
    if "chat_id" in dct:
        dct["chat_id"] = int(dct["chat_id"])
        return Chat(**dct)
    new_d = {}
    for k, v in dct.items():
        if isinstance(k, str) and (k.isnumeric() or k[0] == "-" and k[1:].isnumeric()):
            new_d[int(k)] = v
        else:
            new_d[k] = v
    return new_d


def make_user(d: dict) -> User:
    user_params = User.__annotations__.keys()
    user_dict = {}
    if "user_id" not in d and "id" in d:
        d["user_id"] = d["id"]
    user_dict = {k: v for k, v in d.items() if k in user_params}
    return User(**user_dict)
