import logging
import os

import dotenv  # type: ignore


dotenv.load_dotenv()
LOGGING_LEVEL = int(os.getenv("LOGGING_LEVEL", logging.INFO))
TG_API_URL = "https://api.telegram.org"
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
POLL_TIMEOUT = int(os.getenv("POLL_TIMEOUT", 60))

JSON_URL = "https://json.extendsclass.com/bin/"
JSON_SECURITY_KEY = os.environ["JSON_SECURITY_KEY"]
JSON_BIN_ID = os.environ["JSON_BIN_ID"]

SOCIAL_CREDIT_INCREMENT = 20

greeting_sticker = "CAADAgADTgUAAsiuFQMWhq_Msw3cOgI"
positive_credit_sticker_id = "AgADAgADf3BGHA"
negative_credit_sticker_id = "AgADAwADf3BGHA"

MY_BOTS = ("mks_nechat_bot", "mks_test_bot")

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
    "\U0001F436",  # 🐶
    "\U0001F415",  # 🐕
    "\U0001F9AE",  # 🦮
    "\U0001F415\U0000200D\U0001F9BA",  # 🐕‍🦺
    "\U0001F429",  # 🐩
)
random_frog = (
    "лягушка",
    "легушка",
    "легушька",
    "легущька",
    "ле гушька",
    "жаба",
    "жабка",
    "жяба",
    "жабкин",
    "среда",
    "\U0001F438",  # 🐸
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

glory_to_ukraine = ("слава украине", "слава Україні")
glory_to_ukraine_response = "ГЕРОЯМ СЛАВА! \U0001F1FA\U0001F1E6"

tractor_driver = "триста"

change_title_prefixes = ("ето не чат", "ето нечат")

no_means_no = "нет"

social_credit_command = "/show_social_credit_scores"
add_birthday_command = "/add_birthday"
list_all_birthdays_command = "/all_birthdays"
location_command = "/change_location"
where_all_command = "/where_all"
report_message_delete_delay = 60
