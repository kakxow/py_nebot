import random
from typing import Optional

from . import constants, get_dog, notion_utils

__all__ = [
    "ukraine",
    # "swearing",
    "hate_speech",
    "corgi",
    "shibe",
    "random_dog",
    "toy",
    "pug",
    "terrier",
    "trista",
    "net",
    "social_credit"
]

from .predicates import (
    is_message_contains_words,
    is_message_ends_with_word,
    is_message_contains_phrases,
)


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


async def base_dog_trigger(
    url: str, msg: dict, *trigger_words: str
) -> Optional[str]:
    message = msg.get("text", "").lower()
    if is_message_contains_words(message, *trigger_words):
        return await get_dog.get(url)
    return None


async def random_dog(msg: dict) -> Optional[str]:
    random_dog_url = "https://dog.ceo/api/breeds/image/random"
    return await base_dog_trigger(random_dog_url, msg, *constants.random_dog)


async def corgi(msg: dict) -> Optional[str]:
    corgi_url = "https://dog.ceo/api/breed/corgi/images/random"
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
    if message == constants.social_credit_command:
        return notion_utils.get_all_scores_pretty()
    return None


async def social_credit(msg: dict) -> Optional[str]:
    sticker = msg.get("sticker", "")
    reply_message = msg.get("reply_to_message", "")
    print(sticker)
    if sticker and reply_message:
        sticker_id = sticker["file_unique_id"]
        print(sticker_id)
        reply_user = reply_message["from"]  # No get here, reply should have this field in a chat.
        print(reply_user)
        if sticker_id == constants.positive_credit_sticker_id:
            notion_utils.add_credits_or_record(reply_user, constants.SOCIAL_CREDIT_INCREMENT)
        elif sticker_id == constants.negative_credit_sticker_id:
            notion_utils.add_credits_or_record(reply_user, -constants.SOCIAL_CREDIT_INCREMENT)
    return None
