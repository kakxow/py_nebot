import random
from typing import Optional

from . import constants, get_dog
from . import trello_calendar, trello_social_credit


__all__ = [
    # "ukraine",
    # "swearing",
    # "hate_speech",
    "corgi",
    "shibe",
    # "random_dog",
    # "toy",
    # "pug",
    # "terrier",
    # "trista",
    # "net",
    "social_credit",
    "show_social_credit",
    "add_birthday",
    # "congrats_today_birthdays"
]

from .predicates import (
    is_message_contains_words,
    is_message_ends_with_word,
    is_message_contains_phrases,
    is_message_startswith,
    is_date
)


async def ukraine(msg: dict, bot) -> Optional[str]:
    message = msg.get("text", "").lower()
    if is_message_contains_phrases(message, *constants.glory_to_ukraine):
        return constants.glory_to_ukraine_response
    return None


async def swearing(msg: dict, bot) -> Optional[str]:
    message = msg.get("text", "").lower()
    if is_message_contains_words(message, *constants.trash):
        return constants.trash_response
    return None


async def hate_speech(msg: dict, bot) -> Optional[str]:
    message = msg.get("text", "").lower()
    is_hate_speech = is_message_contains_words(message, *constants.hate_speech)
    if is_hate_speech:
        return constants.hate_speech_response
    return None


async def trista(msg: dict, bot) -> Optional[str]:
    message = msg.get("text", "").lower()
    if is_message_ends_with_word(message, constants.tractor_driver):
        return random.choice(constants.trista)
    return None


async def net(msg: dict, bot) -> Optional[str]:
    message = msg.get("text", "").lower()
    if is_message_ends_with_word(message, constants.no_means_no):
        return random.choice(constants.net)
    return None


async def base_dog_trigger(
    url: str, msg: dict, *trigger_words: str
) -> Optional[str]:
    message = msg.get("text", "").lower()
    if is_message_contains_words(message, *trigger_words):
        return await get_dog.get(url)
    return None


async def random_dog(msg: dict, bot) -> Optional[str]:
    random_dog_url = "https://dog.ceo/api/breeds/image/random"
    return await base_dog_trigger(random_dog_url, msg, *constants.random_dog)


async def corgi(msg: dict, bot) -> Optional[str]:
    corgi_url = "https://dog.ceo/api/breed/corgi/images/random"
    return await base_dog_trigger(corgi_url, msg, *constants.corgi)


async def shibe(msg: dict, bot) -> Optional[str]:
    shibe_url = "http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=false"
    return await base_dog_trigger(shibe_url, msg, *constants.shibe)


async def toy(msg: dict, bot) -> Optional[str]:
    toy_url = "https://dog.ceo/api/breed/terrier/toy/images/random"
    return await base_dog_trigger(toy_url, msg, *constants.toy)


async def pug(msg: dict, bot) -> Optional[str]:
    pug_url = "https://dog.ceo/api/breed/pug/images/random"
    return await base_dog_trigger(pug_url, msg, *constants.pug)


async def terrier(msg: dict, bot) -> Optional[str]:
    terrier_url = "https://dog.ceo/api/breed/terrier/images/random"
    return await base_dog_trigger(terrier_url, msg, *constants.terrier)


async def show_social_credit(msg: dict, bot) -> Optional[str]:
    message = msg.get("text", "").lower()
    chat_id = int(msg.get("chat", {}).get("id", ""))
    if is_message_startswith(message, constants.social_credit_command):
        print("Getting all credit scores.")
        return trello_social_credit.get_all_scores_pretty(chat_id)
    return None


async def social_credit(msg: dict, bot) -> Optional[str]:
    sticker = msg.get("sticker", "")
    reply_message = msg.get("reply_to_message", "")
    chat_id = int(msg.get("chat", {}).get("id", ""))
    if sticker and reply_message:
        sticker_id = sticker["file_unique_id"]
        reply_user = reply_message["from"]
        message_user = msg["from"]
        if reply_user == message_user:
            return None
        if sticker_id == constants.positive_credit_sticker_id:
            print("Adding credit score.")
            trello_social_credit.add_credits_or_record(chat_id, reply_user, constants.SOCIAL_CREDIT_INCREMENT)
        elif sticker_id == constants.negative_credit_sticker_id:
            print("Substracting credit score.")
            trello_social_credit.add_credits_or_record(chat_id, reply_user, -constants.SOCIAL_CREDIT_INCREMENT)
    return None


async def add_birthday(msg: dict, bot) -> Optional[str]:
    message = msg.get("text", "").lower()
    chat_id = int(msg.get("chat", {}).get("id", ""))
    if is_message_startswith(message, constants.add_birthday_command):
        _, date = message.split()
        if not is_date(date):
            return "Please enter valid date - DD.MM"
        user = msg["from"]
        trello_calendar.update_or_add_birthday_card(chat_id, user, date)
        return "Your birthday has been added"
    return None


async def congrats_today_birthdays(msg: dict, bot) -> Optional[str]:
    message = msg.get("text", "").lower()
    chat_id = int(msg.get("chat", {}).get("id", ""))
    if is_message_startswith(message, "/check"):
        ids = trello_calendar.get_today_birthdays(chat_id)
        if ids:
            chat_members = [await bot.get_chat_member(chat_id, int(id)) for id in ids]
            usernames = [f'@{chat_member.get("user").get("username", "")}' for chat_member in chat_members]
            text_usernames = ", ".join(usernames)
            return f"Happy birthday {text_usernames}!"
    return None
