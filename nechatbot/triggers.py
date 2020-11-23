import random
from typing import Optional

from . import constants, get_dog

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
]

from .predicates import is_message_contains_words, is_message_endswith, is_message_contains_phrases


async def ukraine(message: str) -> Optional[str]:
    if is_message_contains_phrases(message, *constants.glory_to_ukraine):
        return constants.glory_to_ukraine_response
    return None


async def swearing(message: str) -> Optional[str]:
    if is_message_contains_words(message, *constants.trash):
        return constants.trash_response
    return None


async def hate_speech(message: str) -> Optional[str]:
    is_hate_speech = is_message_contains_words(message, *constants.hate_speech)
    if is_hate_speech:
        return constants.hate_speech_response
    return None


async def trista(message: str) -> Optional[str]:
    if is_message_endswith(message, constants.tractor_driver):
        return random.choice(constants.trista)
    return None


async def net(text: str) -> Optional[str]:
    if is_message_endswith(text, constants.no_means_no):
        return random.choice(constants.net)
    return None


async def base_dog_trigger(url: str, message: str, *trigger_words: str) -> Optional[str]:
    if is_message_contains_words(message, *trigger_words):
        return await get_dog.get(url)
    return None


async def random_dog(message: str) -> Optional[str]:
    random_dog_url = "https://dog.ceo/api/breeds/image/random"
    return await base_dog_trigger(random_dog_url, message, *constants.random_dog)


async def corgi(message: str) -> Optional[str]:
    corgi_url = "https://dog.ceo/api/breed/corgi/images/random"
    return await base_dog_trigger(corgi_url, message, *constants.corgi)


async def shibe(message: str) -> Optional[str]:
    shibe_url = "http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=false"
    return await base_dog_trigger(shibe_url, message, *constants.shibe)


async def toy(message: str) -> Optional[str]:
    toy_url = "https://dog.ceo/api/breed/terrier/toy/images/random"
    return await base_dog_trigger(toy_url, message, *constants.toy)


async def pug(message: str) -> Optional[str]:
    pug_url = "https://dog.ceo/api/breed/pug/images/random"
    return await base_dog_trigger(pug_url, message, *constants.pug)


async def terrier(message: str) -> Optional[str]:
    terrier_url = "https://dog.ceo/api/breed/terrier/images/random"
    return await base_dog_trigger(terrier_url, message, *constants.terrier)
