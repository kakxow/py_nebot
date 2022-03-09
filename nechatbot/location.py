import json

from . import trello_main


locations = {
    "msk": ("@мск", "@msk"),
    "spb": ("@спб", "@spb"),
    "baku": ("@баку", "@baku", "@bak", "@бак"),
    "ist": ("@ist", "@istanbul", "@стамбул"),
    "tbl": ("@tbl", "@tbilisi", "@тбилиси", "@тбл"),
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
