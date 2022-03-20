import hashlib
from json.decoder import JSONDecodeError
from typing import Dict, List, TypedDict, Union
from urllib.parse import urljoin, quote
import logging

import requests

from constants import JSON_API_KEY, JSON_SECURITY_KEY, JSON_URL, JSON_ID


logger = logging.getLogger(__name__)
headers = {
    "Api-key": JSON_API_KEY,
    "Security-key": JSON_SECURITY_KEY,
    "Private": "true",
}

ChatId = Union[str, int]
UserId = ChatId
User = TypedDict(
    "User",
    {
        "user_id_hashed": str,
        "first_name": str,
        "last_name": str,
        "username": str,
        "location": str,
        "credit": int,
        "birthday": str,
    },
)
User2 = TypedDict(
    "User",
    {
        "user_id_hashed": str,
        "chat_ids": List[ChatId],
        "first_name": str,
        "last_name": str,
        "username": str,
        "location": str,
        "credit": int,
        "birthday": str,
    },
)
Chat = TypedDict("Chat", {"chat_id": ChatId, "users": Dict[UserId, User]})
StorageData = Dict[ChatId, Chat]


def hash_user_id(user_id: ChatId) -> str:
    return hashlib.md5(str(user_id).encode("utf-8")).hexdigest()


def _load_data(json_id: str = JSON_ID) -> StorageData:
    url = urljoin(JSON_URL, quote(JSON_ID))
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    try:
        data: StorageData = response.json()
    except JSONDecodeError:
        logger.critical("Error in json decoding, probably empty? %s", JSON_ID)
        data = {}
    return data


def _update_data(data: StorageData) -> StorageData:
    url = urljoin(JSON_URL, quote(JSON_ID))
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    new_data: StorageData = response.json()
    return new_data


def get_users_for_chat(chat_id: ChatId) -> Dict[UserId, User]:
    data = _load_data()
    chat: Chat = data.get(chat_id, {"chat_id": 0, "users": {}})
    return chat["users"]


def get_chat_ids() -> List[ChatId]:
    data = _load_data()
    return list(data.keys())


def get_user(chat_id: ChatId, user_id: UserId) -> User:
    users = get_users_for_chat(chat_id)
    return users.get(user_id, {})  # type: ignore [typeddict-item]


def update_user(chat_id: ChatId, user_id: UserId, new_user_data: dict) -> User:
    data = _load_data()
    user = data.get(chat_id).get("users").get(user_id)

    user = get_user(chat_id, user_id)
    user.update(new_user_data)


class Storage:
    def __init__(self) -> None:
        self.url = urljoin(JSON_URL, quote(JSON_ID))
        self.data = self._load_data()

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

    def fetch_users_for_chat(self, chat_id: ChatId) -> Dict[UserId, User]:
        chat: Chat = self.data.get(chat_id, {"chat_id": 0, "users": {}})
        return chat["users"]

    def get_chat_ids(self) -> List[ChatId]:
        return list(self.data.keys())

    def get_users_for_chat(self, chat_id: ChatId) -> Dict[UserId, User]:
        chat: Chat = self.data.get(chat_id, {"chat_id": 0, "users": {}})
        return chat["users"]

    def get_user(self, chat_id: ChatId, user_id: UserId) -> User:
        users = self.get_users_for_chat(chat_id)
        return users.get(user_id, {})  # type: ignore [typeddict-item]

    def update_user(
        self, chat_id: ChatId, user_id: UserId, new_user_data: User
    ) -> User:
        self.data[chat_id]["users"][user_id] = new_user_data
        self._upload_data()
        return new_user_data

    def delete_user_everywhere(self) -> None:
        pass

    def delete_user_entry(self, entry):
        pass
