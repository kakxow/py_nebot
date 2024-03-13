from dataclasses import dataclass, field
from itertools import groupby

from .db import Session, update_user
from .nechat_db_types import User


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
    Location("tbl", "Tbilisi", ("tbl", "tbilisi", "тбилиси", "тбл", "tbs", "tbi")),
    Location("yer", "Yerevan", ("yer", "yerevan", "ереван", "ере")),
    Location("ala", "Almaty", ("ala", "almt", "almaty", "алматы", "ата")),
    Location(
        "ovb",
        "Novosibirsk",
        ("ovb", "sib", "nsb", "novosibirsk", "новосибирск", "сиб", "новосиб"),
    ),
    Location("tmb", "Tambov", ("tmb", "tambov", "тамбов", "тмб")),
    Location("ber", "Berlin", ("ber", "berlin", "берлин", "бер")),
    Location("hag", "Den Haag", ("hag", "rtm", "denhaag", "гаага", "хаг", "hague")),
    Location("remove", "remove", ("remove",)),
)

tag_to_name = {loc.name: loc.city_name for loc in locations}

locations_text = "\n".join(
    (f"{loc.city_name} - {', '.join(loc.registration_tags)}" for loc in locations)
)


def change_location(chat_id: int, user: dict, location: str) -> None:
    update_user(chat_id, user, {"location": location})


def get_people_from_location(chat_id: int, location: str) -> list[User]:
    with Session() as session:
        users = (
            session.query(User)
            .filter(User.chat == chat_id, User.location == location)
            .all()
        )

    return users


def get_locations_with_people(chat_id: int) -> dict[str, list[User]]:
    """city_name : [{"id": , "first_name": , "last_name": , "username": , "location": }, ...]"""
    users_in_location: dict[str, list[User]] = {}
    with Session() as session:
        users = (
            session.query(User)
            .filter(User.chat == chat_id)
            .order_by(User.location)
            .all()
        )
        for location, group in groupby(users, lambda u: u.location):
            city_name = tag_to_name.get(location, "remove")
            users_in_location[city_name] = list(group)
        users_in_location.pop("remove", None)
        return users_in_location
