from .nechat_types import User
from . import storage, location


def user_tags(user: User) -> set[str]:
    location_tags = set(location.name_to_tag.get(user.location, ()))
    return set(user.tags) | location_tags


def fetch_users_with_tags(chat_id: int, tags: set) -> list[User]:
    chats = storage.get_chats()
    if chat_id not in chats:
        return []
    return [user for user in chats[chat_id].users.values() if tags & user_tags(user)]


def fetch_existing_tags() -> set[str]:
    [{"name": "", "description": "", "tags": ["", "", ""]}]
    tags = []
    for tag in storage.fetch_storage("tags"):
        tags.extend(tag["tags"])
    return set(tags)


def validate_tags(tags: set[str]) -> tuple[set[str], set[str]]:
    existing_tags = fetch_existing_tags()
    valid_tags = tags & existing_tags
    non_valid_tags = tags - existing_tags
    return valid_tags, non_valid_tags
