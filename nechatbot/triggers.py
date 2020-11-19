import random
import re
from typing import Tuple

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


def words_in_text(words: Tuple[str, ...], text: str) -> bool:
    return any(word in text for word in words)


def words_in_text_re(words: Tuple[str, ...], text: str) -> bool:
    pattern = r'\b' + r'\b|\b'.join(words) + r'\b'
    match = re.search(pattern, text, re.I)
    return bool(match)


async def ukraine(text: str) -> str:
    return "ГЕРОЯМ СЛАВА! \U0001F1FA\U0001F1E6" if "слава украине" in text else ""


async def swearing(text: str) -> str:
    is_swearing = words_in_text(constants.trash, text.split())
    return "а давайте не материться" if is_swearing else ""


async def hate_speech(text: str) -> str:
    is_hate_speech = words_in_text(constants.hate_speech, text.split())
    return "это хейтспич приятель" if is_hate_speech else ""


async def trista(text: str) -> str:
    return random.choice(constants.trista) if "триста" in text else ""


async def net(text: str) -> str:
    pattern_net = r'(\W|^)нет$'
    match = re.search(pattern_net, text)
    return random.choice(constants.net) if match else ""


async def random_dog(text: str) -> str:
    random_dog_url = "https://dog.ceo/api/breeds/image/random"
    has_random_dog = words_in_text(constants.random_dog, text.split())
    return await get_dog.get(random_dog_url) if has_random_dog else ""


async def corgi(text: str) -> str:
    corgi_url = "https://dog.ceo/api/breed/corgi/images/random"
    has_corgi = words_in_text(constants.corgi, text.split())
    return await get_dog.get(corgi_url) if has_corgi else ""


async def shibe(text: str) -> str:
    shibe_url = "http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=false"
    has_shibe = words_in_text(constants.shibe, text.split())
    return await get_dog.get(shibe_url) if has_shibe else ""


async def toy(text: str) -> str:
    toy_url = "https://dog.ceo/api/breed/terrier/toy/images/random"
    has_toy = words_in_text(constants.toy, text.split())
    return await get_dog.get(toy_url) if has_toy else ""


async def pug(text: str) -> str:
    pug_url = "https://dog.ceo/api/breed/pug/images/random"
    has_pug = words_in_text(constants.pug, text.split())
    return await get_dog.get(pug_url) if has_pug else ""


async def terrier(text: str) -> str:
    terrier_url = "https://dog.ceo/api/breed/terrier/images/random"
    has_terrier = words_in_text(constants.terrier, text.split())
    return await get_dog.get(terrier_url) if has_terrier else ""
