import os

import dotenv

from . import trigger

dotenv.load_dotenv()
TG_API_URL = 'https://api.telegram.org'
BOT_TOKEN = os.getenv('BOT_TOKEN', '')

greeting_sticker = 'CAADAgADTgUAAsiuFQMWhq_Msw3cOgI'
hate_speech = [
    "пидор",
    "пидр",
    "нигер",
    "нигга",
]
shiba = [
    "сиба",
    "сибу",
    "шиба",
    "сибушка",
    "шибушка",
    "шибой",
]
corgi = [
    "корги",
    "коржик",
]
random_dog = [
  "песель",
  "пёсель",
  "собака",
  "пёс",
  "пёса",
  "догич",
  "догислав",
  "дог",
  "собак",
  "собакен",
  "собакич",
  "догислав",
  "собакевич",
  "пепс",
  "догос",
  "доггос",
  "доггер",
  "догич",
]
net = [
  "минет",
  "омлет",
  "паштет",
  "паштет",
  "менталитет",
  "авиабилет",
  "интернет",
  "бронежилет",
  "банкет",
  "суверенитет",
  "туалет",
  "портрет",
  "фальцет",
  "жакет",
  "прокурор въебал пять лет",
  "СОДОМИТА ОТВЕТ",
  "СОДОМИТА ОТВЕТ",
  "СОДОМИТА ОТВЕТ",
  "СОДОМИТА ОТВЕТ",
  "СОДОМИТА ОТВЕТ",
  "СОДОМИТА ОТВЕТ",
  "хуй зажало в турникет",
]
trista = [
  "хуйни в ссылку декабриста",
  "благодарите программиста",
  "абстрагируйся от суеты, достигнув с космосом единства",
  "метни бутылку в альпиниста",
]


triggers = [
    (['слава украине'], trigger.glory_to_heroes),
    (['пизда'], trigger.trash_talk),
    (hate_speech, trigger.hate_speech),
    (corgi, trigger.corgi),
    (shiba, trigger.shiba),
    (random_dog, trigger.random),
    (["той"], trigger.toy),
    (['мопс'], trigger.pug),
    (['триста'], trigger.trista),
    (['терьер'], trigger.terrier),
]
