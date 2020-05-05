import random as rnd
from typing import List

from .get_dog import get_dog


async def glory_to_heroes() -> str:
    return "ГЕРОЯМ СЛАВА!"


async def trash_talk() -> str:
    return "а давайте не материться"


async def hate_speech() -> str:
    return "это хейтспич приятель"


async def corgi() -> str:
    return await get_dog("corgi")


async def shiba() -> str:
    return await get_dog("shiba")


async def random() -> str:
    return await get_dog("random")


async def toy() -> str:
    return await get_dog("toy")


async def pug() -> str:
    return await get_dog("pug")


async def trista(enum: List[str]) -> str:
    return rnd.choice(enum)
