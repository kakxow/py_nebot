import random
from typing import Optional

from .location import (
    change_location,
    get_people_from_location,
    locations,
    locations_text,
)
from . import constants, get_dog, get_frog
from . import calendar, social_credit
from .predicates import (
    is_message_contains_words,
    is_message_contains_words_and_emojis,
    is_message_ends_with_word,
    is_message_contains_phrases,
    is_message_startswith,
    is_date,
)


__all__ = [
    "ukraine",
    # "swearing",
    "hate_speech",
    "corgi",
    "shibe",
    "random_dog",
    "random_frog",
    # "toy",
    "pug",
    "terrier",
    "trista",
    "net",
    "add_social_credit",
    "show_social_credit",
    "add_birthday",
    "list_all_birthdays",
    "add_birthday_inline",
    "add_location2",
    "ping_location2",
]
auto_delete_list = ["show_social_credit"]


async def ukraine(msg: dict) -> Optional[str]:
    message = msg.get("text", "").lower()
    if is_message_contains_phrases(message, *constants.glory_to_ukraine):
        return constants.glory_to_ukraine_response
    return None


async def swearing(msg: dict) -> Optional[str]:
    message = msg.get("text", "").lower()
    if is_message_contains_words(message, *constants.trash):
        return constants.trash_response
    return None


async def hate_speech(msg: dict) -> Optional[str]:
    message = msg.get("text", "").lower()
    is_hate_speech = is_message_contains_words(message, *constants.hate_speech)
    if is_hate_speech:
        return constants.hate_speech_response
    return None


async def trista(msg: dict) -> Optional[str]:
    message = msg.get("text", "").lower()
    if is_message_ends_with_word(message, constants.tractor_driver):
        return random.choice(constants.trista)
    return None


async def net(msg: dict) -> Optional[str]:
    message = msg.get("text", "").lower()
    if is_message_ends_with_word(message, constants.no_means_no):
        return random.choice(constants.net)
    return None


async def base_dog_trigger(url: str, msg: dict, *trigger_words: str) -> Optional[str]:
    message = msg.get("text", "").lower()
    if is_message_contains_words_and_emojis(message, *trigger_words):
        return await get_dog.get(url)
    return None


async def random_frog(msg: dict) -> Optional[str]:
    random_frog_url = "https://www.generatormix.com/random-frogs"
    message = msg.get("text", "").lower()
    if is_message_contains_words_and_emojis(message, *constants.random_frog):
        return await get_frog.get(random_frog_url)
    return None


async def random_dog(msg: dict) -> Optional[str]:
    random_dog_url = "https://dog.ceo/api/breeds/image/random"
    return await base_dog_trigger(random_dog_url, msg, *constants.random_dog)


async def corgi(msg: dict) -> Optional[str]:
    corgi_url = random.choice(
        (
            "https://dog.ceo/api/breed/corgi/images/random",
            "https://dog.ceo/api/breed/pembroke/images/random",
        )
    )
    # corgi_url = "https://dog.ceo/api/breed/corgi/images/random"
    return await base_dog_trigger(corgi_url, msg, *constants.corgi)


async def shibe(msg: dict) -> Optional[str]:
    shibe_url = "http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=false"
    return await base_dog_trigger(shibe_url, msg, *constants.shibe)


async def toy(msg: dict) -> Optional[str]:
    toy_url = "https://dog.ceo/api/breed/terrier/toy/images/random"
    return await base_dog_trigger(toy_url, msg, *constants.toy)


async def pug(msg: dict) -> Optional[str]:
    pug_url = "https://dog.ceo/api/breed/pug/images/random"
    return await base_dog_trigger(pug_url, msg, *constants.pug)


async def terrier(msg: dict) -> Optional[str]:
    terrier_url = "https://dog.ceo/api/breed/terrier/images/random"
    return await base_dog_trigger(terrier_url, msg, *constants.terrier)


async def show_social_credit(msg: dict) -> Optional[str]:
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    if is_message_startswith(message, constants.social_credit_command):
        print("Getting all credit scores.")
        return social_credit.get_all_scores_pretty(chat_id)
    return None


async def add_social_credit(msg: dict) -> Optional[str]:
    sticker = msg.get("sticker", {})
    reply_message = msg.get("reply_to_message", {})
    chat_id = msg["chat"]["id"]
    if sticker and reply_message:
        sticker_id = sticker["file_unique_id"]
        reply_user = reply_message["from"]
        message_user = msg["from"]
        if reply_user == message_user:
            return None
        if sticker_id == constants.positive_credit_sticker_id:
            social_credit.update_or_add_social_credit(
                chat_id, reply_user, constants.SOCIAL_CREDIT_INCREMENT
            )
        elif sticker_id == constants.negative_credit_sticker_id:
            social_credit.update_or_add_social_credit(
                chat_id, reply_user, -constants.SOCIAL_CREDIT_INCREMENT
            )
    return None


async def add_birthday(msg: dict) -> Optional[str]:
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    if is_message_startswith(message, constants.add_birthday_command):
        command_args = message.split()
        if len(command_args) >= 2:
            _, date, *_ = message.split()
            if is_date(date):
                user = msg["from"]
                action = calendar.update_or_add_birthday(chat_id, user, date)
                return f"{action} {user['first_name']}'s card with birthday date {date}"
        return "Please enter valid date - DD.MM"
    return None


async def add_birthday_inline(msg: dict) -> Optional[str]:
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    via_bot = msg.get("via_bot", {})
    bot_name = via_bot.get("first_name", "")

    if bot_name in constants.MY_BOTS:
        date = message[-5:]
        if is_date(date):
            user = msg["from"]
            calendar.update_or_add_birthday(chat_id, user, date)
    return None


async def list_all_birthdays(msg: dict) -> Optional[str]:
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    if is_message_startswith(message, constants.list_all_birthdays_command):
        return calendar.get_all_birthdays_pretty(chat_id)
    return None


async def add_location2(msg: dict) -> Optional[str]:
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    if is_message_startswith(message, constants.location_command):
        user = msg["from"]
        _, location, *_ = message.split()
        for loc in locations:
            if location in loc.registration_tags:
                change_location(chat_id, user, loc.name)
                return f"Location changed to {loc.city_name}"
        return f'Location "{location}" is not in a list, try these or ask Max to add new\n{locations_text}'
    return None


async def ping_location2(msg: dict) -> Optional[str]:
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    for loc in locations:
        if is_message_contains_phrases(message, *loc.mention_tags):
            id_usernames = get_people_from_location(chat_id, loc.name)
            return ", ".join(
                [
                    f'<a href="tg://user?id={user_id}">{username}</a>'
                    for user_id, username in id_usernames
                ]
            )
    return None
