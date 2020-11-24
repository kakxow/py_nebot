import random
import string

import pytest  # type: ignore

from nechatbot import triggers
from nechatbot import constants

# pytest -x -n 5 --pdb


@pytest.fixture(scope="function")
def random_string():
    random.seed()
    random_chars = (random.choice(string.ascii_letters) for _ in range(15))
    return ''.join(random_chars)


@pytest.mark.asyncio
async def test_ukraine(random_string):
    text = random_string + "Слава украине!" + random_string
    result = await triggers.ukraine(text.lower())
    assert result == "ГЕРОЯМ СЛАВА! \U0001F1FA\U0001F1E6"


@pytest.mark.parametrize('bad_word', constants.trash)
@pytest.mark.asyncio
async def test_swearing(bad_word, random_string):
    text = random_string + ' ' + bad_word + ' ' + random_string
    result = await triggers.swearing(text.lower())
    assert result == "а давайте не материться"


@pytest.mark.parametrize('hate_speech', constants.hate_speech)
@pytest.mark.asyncio
async def test_hate_speech(hate_speech, random_string):
    text = random_string + ' ' + hate_speech + ' ' + random_string
    result = await triggers.hate_speech(text.lower())
    assert result == "это хейтспич приятель"


@pytest.mark.asyncio
async def test_trista(random_string):
    text = random_string + " триста"
    result = await triggers.trista(text.lower())
    assert result in constants.trista


@pytest.mark.asyncio
async def test_trista_mid_text(random_string):
    text = f"{random_string} триста {random_string}"
    result = await triggers.trista(text.lower())
    assert result is None


@pytest.mark.asyncio
async def test_net(random_string):
    text = random_string + " нет"
    text = await triggers.net(text)
    assert text in constants.net


@pytest.mark.asyncio
async def test_net_mid_text(random_string):
    text = random_string + " нет " + random_string
    text = await triggers.net(text)
    assert text is None


@pytest.mark.asyncio
async def test_net_only(random_string):
    text = "нет"
    text = await triggers.net(text)
    assert text in constants.net


@pytest.mark.asyncio
async def test_net_old(random_string):
    text = random_string + "нет"
    text = await triggers.net(text)
    assert text is None


@pytest.mark.parametrize('random_dog', constants.random_dog)
@pytest.mark.asyncio
async def test_random_dog(random_dog, random_string):
    text = random_string + ' ' + random_dog + ' ' + random_string
    result = await triggers.random_dog(text)
    assert "dog.ceo" in result


@pytest.mark.parametrize('random_dog', constants.random_dog)
@pytest.mark.asyncio
async def test_random_dog_old(random_dog, random_string):
    text = random_string + random_dog + random_string
    result = await triggers.random_dog(text)
    assert result is None


@pytest.mark.parametrize('corgi', constants.corgi)
@pytest.mark.asyncio
async def test_corgi(corgi, random_string):
    text = random_string + ' ' + corgi + ' ' + random_string
    result = await triggers.corgi(text)
    assert "corgi" in result


@pytest.mark.parametrize('shibe', constants.shibe)
@pytest.mark.asyncio
async def test_shibe(shibe, random_string):
    text = random_string + ' ' + shibe + ' ' + random_string
    result = await triggers.shibe(text)
    assert "shibe" in result


@pytest.mark.parametrize('toy', constants.toy)
@pytest.mark.asyncio
async def test_toy(toy, random_string):
    text = random_string + ' ' + toy + ' ' + random_string
    result = await triggers.toy(text)
    assert "toy" in result


@pytest.mark.parametrize('pug', constants.pug)
@pytest.mark.asyncio
async def test_pug(pug, random_string):
    text = random_string + ' ' + pug + ' ' + random_string
    result = await triggers.pug(text)
    assert "pug" in result


@pytest.mark.parametrize('terrier', constants.terrier)
@pytest.mark.asyncio
async def test_terrier(terrier, random_string):
    text = random_string + ' ' + terrier + ' ' + random_string
    result = await triggers.terrier(text)
    assert "terrier" in result
