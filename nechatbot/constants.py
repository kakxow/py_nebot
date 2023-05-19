import logging
import os

import dotenv  # type: ignore


dotenv.load_dotenv()
LOGGING_LEVEL = int(os.getenv("LOGGING_LEVEL", logging.INFO))
TG_API_URL = "https://api.telegram.org"
BOT_TOKEN = os.environ["BOT_TOKEN"]
BASE_URL = f"{TG_API_URL}/bot{BOT_TOKEN}"
POLL_TIMEOUT = int(os.getenv("POLL_TIMEOUT", 60))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
POLL = os.getenv("POLL", 0)

SECURITY_KEY = JSON_SECURITY_KEY = os.environ["JSON_SECURITY_KEY"]

greeting_sticker = "CAADAgADTgUAAsiuFQMWhq_Msw3cOgI"
positive_credit_sticker_id = "AgADAgADf3BGHA"
negative_credit_sticker_id = "AgADAwADf3BGHA"

MY_BOTS = ("mks_nechat_bot", "mks_test_bot")

maintainer = "@umarth"

birthday_error_reply = "Please reply with valid date - DD.MM"
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

report_message_delete_delay = 60

commands = {
    "add_birthday_command": {
        "command": "/add_birthday",
        "description": "Добавить своё ДР, чтобы бот потом всем напомнил. Укажи его в формате ДД.ММ через пробел после команды. Например, /add_birthday 03.09. Либо ответьте боту с корректной датой :)",
    },
    "list_all_birthdays_command": {
        "command": "/all_birthdays",
        "description": f"Вывести все ДР (автоудалится через {report_message_delete_delay} секунд)",
    },
    "location_command": {
        "command": "/change_location",
        "description": "Добавить свою локацию, потом тебя можно будет тегнуть. Например, /change_location tbl. Для полного списка локаций  - /change_location",
    },
    "where_all_command": {
        "command": "/where_all",
        "description": f"Вывести кто где (автоудалится через {report_message_delete_delay} секунд)",
    },
    "help_command": {
        "command": "/help",
        "description": "Описание бота.",
    },
    "list_tags": {
        "command": "/list_tags",
        "description": "Вывести все тэги и меншены к ним.",
    },
    "assign_tags": {
        "command": "/assign_tags",
        "description": "Назначить себе тэг(и), /assign_tags anime freebsd",
    },
    "create_tag": {
        "command": "/create_tag",
        "description": "Создать новый тэг. /create_tag anime nya kawaii",
    },
    "free_tags": {
        "command": "/free_tags",
        "description": "Убрать себе тэг(и). /free_tags anime freebsd",
    },
    "free_all_tags": {
        "command": "/free_all_tags",
        "description": "Убрать себе все тэги.",
    },
    "your_tags": {
        "command": "/your_tags",
        "description": "Посмотреть свои тэги.",
    },
    "update_tag": {
        "command": "/update_tag",
        "description": "Обновить список меншенов тэгу /update_tags anime nya kawaii uwu owo",
    },
    "create_location": {
        "command": "/create_location",
        "description": "Добавить новую локацию /create_location Batumi bat bus btm",
    },
}

commands_for_help = "\n".join(
    [
        f"{element['command']} - {element['description']}"
        for element in commands.values()
    ]
)

help_message = f"""
Привет! Это бот для нечата.
Передразнивает, приветствует новых участников, поздравляет с ДР*, постит лягух и собакенов
Для изменения названия чята, напиши сообщение, начинающееся с "ето не чат" или "ето нечат"
* добавь своё ДР командой

{commands_for_help}

Вопросы по работе бота - {maintainer}
"""
