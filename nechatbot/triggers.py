import random

from . import constants, get_dog


async def ukraine(text: str) -> str:
    return "ГЕРОЯМ СЛАВА!" if "слава украине" in text else ""


async def swearing(text: str) -> str:
    is_swearing = any(word in text for word in constants.trash)
    return "а давайте не материться" if is_swearing else ""


async def hate_speech(text: str) -> str:
    is_hate_speech = any(word in text for word in constants.hate_speech)
    return "это хейтспич приятель" if is_hate_speech else ""


async def corgi(text: str) -> str:
    corgi_url = "https://dog.ceo/api/breed/corgi/cardigan/images/random"
    has_corgi = any(word in text for word in constants.corgi)
    return await get_dog.get(corgi_url) if has_corgi else ""


async def shibe(text: str) -> str:
    shibe_url = "http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=false"
    has_shibe = any(word in text for word in constants.shibe)
    return await get_dog.get(shibe_url) if has_shibe else ""


async def random_dog(text: str) -> str:
    random_dog_url = "https://dog.ceo/api/breeds/image/random"
    has_random_dog = any(word in text for word in constants.random_dog)
    return await get_dog.get(random_dog_url) if has_random_dog else ""


async def toy(text: str) -> str:
    toy_url = "https://dog.ceo/api/breed/terrier/toy/images/random"
    has_toy = any(word in text for word in constants.toy)
    return await get_dog.get(toy_url) if has_toy else ""


async def pug(text: str) -> str:
    pug_url = "https://dog.ceo/api/breed/pug/images/random"
    has_pug = any(word in text for word in constants.pug)
    return await get_dog.get(pug_url) if has_pug else ""


async def terrier(text: str) -> str:
    terrier_url = "https://dog.ceo/api/breed/terrier/images/random"
    has_terrier = any(word in text for word in constants.terrier)
    return await get_dog.get(terrier_url) if has_terrier else ""


async def trista(text: str) -> str:
    return random.choice(constants.trista) if "триста" in text else ""


async def net(text: str) -> str:
    return random.choice(constants.net) if text.endswith("нет") else ""
