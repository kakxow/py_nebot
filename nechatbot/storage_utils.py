import logging
from json.decoder import JSONDecodeError
from typing import Any, Dict, List, Optional, TypedDict, Union
from urllib.parse import quote, urljoin

import requests

from constants import JSON_API_KEY, JSON_ID, JSON_SECURITY_KEY, JSON_URL

logger = logging.getLogger(__name__)
headers = {
    "Api-key": JSON_API_KEY,
    "Security-key": JSON_SECURITY_KEY,
    "Private": "true",
}

ChatId = Union[str, int]
UserId = int

User = TypedDict(
    "User",
    {
        "user_id": UserId,
        "chat_ids": List[ChatId],
        "first_name": str,
        "last_name": str,
        "username": str,
        "location": str,
        "credit": int,
        "birthday": str,
    },
)
StorageData = Dict[UserId, User]


def create_user_from_tg_user(**user_data: Any) -> User:
    return User(
        user_id=user_data["id"],
        chat_ids=[user_data["chat_id"]],
        first_name=user_data["first_name"],
        last_name=user_data.get("last_name", ""),
        username=user_data.get("username", ""),
        location=user_data.get("location", ""),
        credit=user_data.get("credit", 0),
        birthday=user_data.get("birthday", ""),
    )


class Storage:
    def __init__(self) -> None:
        self.url = urljoin(JSON_URL, quote(JSON_ID))
        self.data = self._load_data()
        self.update_schema()

    def _load_data(self) -> StorageData:
        response = requests.get(self.url, headers=headers)
        response.raise_for_status()
        try:
            data: StorageData = response.json()
        except JSONDecodeError:
            logger.critical("Error in json decoding, probably empty? %s", JSON_ID)
            data = {}
        return data

    def _upload_data(self) -> StorageData:
        response = requests.put(self.url, headers=headers, json=self.data)
        response.raise_for_status()
        new_data: StorageData = response.json()
        return new_data

    def update_schema(self) -> None:
        for user in self.data.values():
            for entry, entry_type in User.__annotations__.items():
                user.setdefault(entry, entry_type())
        self._upload_data()

    def get_users_for_chat(self, chat_id: ChatId) -> List[User]:
        chat_users = [
            user for user in self.data.values() if chat_id in user["chat_ids"]
        ]
        return chat_users

    def get_chat_ids(self) -> List[ChatId]:
        chat_ids = {
            chat_id for user in self.data.values() for chat_id in user["chat_ids"]
        }
        return list(chat_ids)

    def get_user(self, user_id: UserId) -> Optional[User]:
        return self.data.get(user_id)

    def update_user(self, user_id: UserId, new_user_data: User) -> User:
        self.data[user_id] = new_user_data
        self._upload_data()
        return new_user_data

    def update_user_attribute(self, user_id: UserId, entry: str, value) -> User:
        if entry in User.__annotations__:
            entry_type = User.__annotations__[entry]
            if isinstance(value, entry_type):
                self.data[user_id][entry] = value
        self._upload_data()
        return self.data[user_id]

    def delete_user(self, user_id: UserId) -> None:
        del self.data[user_id]
        self._upload_data()

    def delete_user_attribute(self, user_id: UserId, entry: str) -> User:
        if entry in User.__annotations__:
            entry_type = User.__annotations__[entry]
            self.data[user_id][entry] = entry_type()
        self._upload_data()
        return self.data[user_id]
