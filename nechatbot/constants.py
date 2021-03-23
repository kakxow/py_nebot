import os

import dotenv  # type: ignore


dotenv.load_dotenv()
TG_API_URL = "https://api.telegram.org"
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_PAGE_URL = os.getenv("PAGE_URL")

TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_SECRET = os.getenv("TRELLO_API_SECRET")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_NECHAT_LIST_ID = os.getenv("TRELLO_NECHAT_LIST_ID")
TRELLO_NECHAT_CALENDAR_ID = os.getenv("TRELLO_NECHAT_CALENDAR_ID")

CREDIT_FIELD_NAME = "credit"
SOCIAL_CREDIT_INCREMENT = 20

greeting_sticker = "CAADAgADTgUAAsiuFQMWhq_Msw3cOgI"
positive_credit_sticker_id = "AgADAgADf3BGHA"
negative_credit_sticker_id = "AgADAwADf3BGHA"


trash = (
    "пизда",
    "хуй",
)
trash_response = "а давайте не материться"
hate_speech = (
    "пидор",
    "пидр",
    "нигер",
    "нигга",
)
hate_speech_response = "это хейтспич приятель"
corgi = (
    "корги",
    "коржик",
)
shibe = (
    "сиба",
    "сибу",
    "шиба",
    "сибушка",
    "шибушка",
    "шибой",
    "биба",
)
random_dog = (
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
    "собачка",
    "собаня",
    "собачька",
)
toy = ("той",)
pug = (
    "пуг",
    "мопс",
)
terrier = ("терьер",)
net = (
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
)
trista = (
    "хуйни в ссылку декабриста",
    "благодарите программиста",
    "абстрагируйся от суеты, достигнув с космосом единства",
    "метни бутылку в альпиниста",
)

glory_to_ukraine = ("слава украине",)
glory_to_ukraine_response = "ГЕРОЯМ СЛАВА! \U0001F1FA\U0001F1E6"

tractor_driver = "триста"

change_title_prefixes = ("ето не чат", "ето нечат")

no_means_no = "нет"

social_credit_command = "/show_social_credit_scores"
add_birthday_command = "/add_my_birthday"
