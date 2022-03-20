from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
import json

from . import trello_main


@dataclass
class Location:
    name: str
    city_name: str
    registration_tags: tuple[str, ...] | tuple[()]
    mention_tags: tuple[str, ...] | tuple[()] = field(init=False)

    def __post_init__(self) -> None:
        self.mention_tags = tuple(f"@{el}" for el in self.registration_tags)


locations = (
    Location("msk", "Moscow", ("мск", "msk", "moscow", "москва")),
    Location("spb", "Saint Petersburg", ("спб", "spb", "питер", "петербург")),
    Location(
        "baku",
        "Baku",
        ("баку", "baku", "bak", "бак"),
    ),
    Location("ist", "Istanbul", ("ist", "istanbul", "стамбул")),
    Location("tbl", "Tbilisi", ("tbl", "tbilisi", "тбилиси", "тбл", "tbs")),
    Location("yer", "Yerevan", ("yer", "yerevan", "ереван", "ере")),
    Location("remove", "remove", ("remove",)),
)

tag_to_name = {loc.name: loc.city_name for loc in locations}

locations_text = "\n".join(
    (f"{loc.city_name} - {', '.join(loc.registration_tags)}" for loc in locations)
)

_locations = {
    "msk": ("@мск", "@msk"),
    "spb": ("@спб", "@spb"),
    "baku": ("@баку", "@baku", "@bak", "@бак"),
    "ist": ("@ist", "@istanbul", "@стамбул"),
    "tbl": ("@tbl", "@tbilisi", "@тбилиси", "@тбл", "@tbs"),
    "yer": ("@yer", "@yerevan", "@ереван", "@ере"),
    "remove": (),
}


def change_location(chat_id: int, user: dict, location: str) -> None:
    location_data = {"location": location}
    card = trello_main.get_card(chat_id, str(user["id"]), "location")
    if card:
        trello_main.update_card(card, location_data, {})
    else:
        trello_main.create_card(chat_id, user, "location", location_data)


def get_people_from_location(chat_id: int, location: str) -> list:
    user_ids = []
    for card in trello_main.get_all_cards(chat_id, "location"):
        card_data = json.loads(card.desc)
        if card_data["location"] == location:
            user_ids.append((card_data["id"], card_data["username"] or "undefined"))
    return user_ids


def get_locations_with_people(chat_id: int) -> dict:
    """city_name : [{"id": , "first_name": , "last_name": , "username": , "location": }, ...]"""
    users_in_location = defaultdict(list)
    for card in trello_main.get_all_cards(chat_id, "location"):
        card_data = json.loads(card.desc)
        city_name = tag_to_name.get(card_data["location"], "undefined")
        users_in_location[city_name].append(card_data)
    users_in_location.pop("undefined", None)
    users_in_location.pop("remove", None)
    return users_in_location
