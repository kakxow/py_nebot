import random

from .location import (
    change_location,
    get_locations_with_people,
    locations,
    locations_text,
)
from . import constants, get_dog, get_frog
from . import calendar, social_credit, tags
from .predicates import (
    extract_tags,
    extract_words,
    is_message_contains_words,
    is_message_contains_words_and_emojis,
    is_message_ends_with_word,
    is_message_contains_phrases,
    is_message_startswith,
    is_date,
)


__all__ = [
    "ukraine",
    # "swearing",
    "hate_speech",
    "corgi",
    "shibe",
    "random_dog",
    "random_frog",
    # "toy",
    "pug",
    "terrier",
    "trista",
    "net",
    # "add_social_credit",
    # "show_social_credit",
    "add_birthday",
    "list_all_birthdays",
    "add_birthday_inline",
    "add_location2",
    "ping_location2",
    "where_all_location",
    "help",
    "add_birthday_from_reply",
    "chat_title",
    "new_chat_member",
]
auto_delete_list = [
    "show_social_credit",
    # "where_all_location",
    # "help",
]


async def ukraine(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_contains_phrases(message, *constants.glory_to_ukraine):
        return constants.glory_to_ukraine_response
    return None


async def swearing(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_contains_words(message, *constants.trash):
        return constants.trash_response
    return None


async def hate_speech(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    is_hate_speech = is_message_contains_words(message, *constants.hate_speech)
    if is_hate_speech:
        return constants.hate_speech_response
    return None


async def trista(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_ends_with_word(message, constants.tractor_driver):
        return random.choice(constants.trista)
    return None


async def net(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_ends_with_word(message, constants.no_means_no):
        return random.choice(constants.net)
    return None


async def base_dog_trigger(url: str, msg: dict, *trigger_words: str) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_contains_words_and_emojis(message, *trigger_words):
        return await get_dog.get(url)
    return None


async def random_frog(msg: dict) -> str | None:
    random_frog_url = "https://www.generatormix.com/random-frogs"
    message = msg.get("text", "").lower()
    if is_message_contains_words_and_emojis(message, *constants.random_frog):
        return await get_frog.get(random_frog_url)
    return None


async def random_dog(msg: dict) -> str | None:
    random_dog_url = "https://dog.ceo/api/breeds/image/random"
    return await base_dog_trigger(random_dog_url, msg, *constants.random_dog)


async def corgi(msg: dict) -> str | None:
    corgi_url = random.choice(
        (
            "https://dog.ceo/api/breed/corgi/images/random",
            "https://dog.ceo/api/breed/pembroke/images/random",
        )
    )
    return await base_dog_trigger(corgi_url, msg, *constants.corgi)


async def shibe(msg: dict) -> str | None:
    shibe_url = "http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=false"
    return await base_dog_trigger(shibe_url, msg, *constants.shibe)


async def toy(msg: dict) -> str | None:
    toy_url = "https://dog.ceo/api/breed/terrier/toy/images/random"
    return await base_dog_trigger(toy_url, msg, *constants.toy)


async def pug(msg: dict) -> str | None:
    pug_url = "https://dog.ceo/api/breed/pug/images/random"
    return await base_dog_trigger(pug_url, msg, *constants.pug)


async def terrier(msg: dict) -> str | None:
    terrier_url = "https://dog.ceo/api/breed/terrier/images/random"
    return await base_dog_trigger(terrier_url, msg, *constants.terrier)


async def show_social_credit(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    if is_message_startswith(
        message, constants.commands["social_credit_command"]["command"]
    ):
        print("Getting all credit scores.")
        return social_credit.get_all_scores_pretty(chat_id)
    return None


async def add_social_credit(msg: dict) -> str | None:
    sticker = msg.get("sticker", {})
    reply_message = msg.get("reply_to_message", {})
    chat_id = str(msg["chat"]["id"])
    if sticker and reply_message:
        sticker_id = sticker["file_unique_id"]
        reply_user = reply_message["from"]
        message_user = msg["from"]
        if reply_user == message_user:
            return None
        if sticker_id == constants.positive_credit_sticker_id:
            social_credit.update_or_add_social_credit(
                chat_id, reply_user, constants.SOCIAL_CREDIT_INCREMENT
            )
        elif sticker_id == constants.negative_credit_sticker_id:
            social_credit.update_or_add_social_credit(
                chat_id, reply_user, -constants.SOCIAL_CREDIT_INCREMENT
            )
    return None


async def add_birthday(msg: dict) -> str | tuple[str, dict] | None:
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    if is_message_startswith(
        message, constants.commands["add_birthday_command"]["command"]
    ):
        command_args = message.split()
        if len(command_args) >= 2:
            _, date, *_ = message.split()
            if is_date(date):
                user = msg["from"]
                calendar.update_or_add_birthday(chat_id, user, date)
                return f"Updated {user['first_name']}'s birthday - {date}"
        force_reply = {"force_reply": True, "selective": True}
        error_reply_args = {
            "text": constants.birthday_error_reply,
            "chat_id": chat_id,
            "reply_to_message_id": msg["message_id"],
            "reply_markup": force_reply,
        }
        return "send_message", error_reply_args
    return None


async def add_birthday_from_reply(msg: dict) -> str | tuple[str, dict] | None:
    reply = msg.get("reply_to_message", {})
    if not reply:
        return None
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    is_reply_from_bot = reply["from"]["is_bot"]
    is_reply_text_birthday = reply.get("text", "") == constants.birthday_error_reply
    if reply and is_reply_from_bot and is_reply_text_birthday:
        if is_date(message):
            user = msg["from"]
            calendar.update_or_add_birthday(chat_id, user, message)
            return f"Updated {user['first_name']}'s birthday - {message}"
        else:
            force_reply = {"force_reply": True, "selective": True}
            error_reply_args = {
                "text": constants.birthday_error_reply,
                "reply_to_message_id": msg["message_id"],
                "reply_markup": force_reply,
            }
            return "send_message", error_reply_args
    return None


async def add_birthday_inline(msg: dict) -> str | None:
    via_bot = msg.get("via_bot", {})
    if not via_bot:
        return None
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    bot_name = via_bot["first_name"]

    if bot_name in constants.MY_BOTS:
        date = message[-5:]
        if is_date(date):
            user = msg["from"]
            calendar.update_or_add_birthday(chat_id, user, date)
    return None


async def list_all_birthdays(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    if is_message_startswith(
        message, constants.commands["list_all_birthdays_command"]["command"]
    ):
        return calendar.get_all_birthdays_pretty(chat_id)
    return None


async def add_location2(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    add_location_error_reply = f"Try these locations or ask {constants.maintainer} to add new\n{locations_text}"
    if is_message_startswith(
        message, constants.commands["location_command"]["command"]
    ):
        command_args = message.split()
        if len(command_args) < 2:
            return add_location_error_reply
        user = msg["from"]
        _, location, *_ = command_args
        for loc in locations:
            if location in loc.registration_tags:
                change_location(chat_id, user, loc.name)
                return f"Location changed to {loc.city_name}"
        return f'Location "{location}" is not in a list. {add_location_error_reply}'
    return None


async def where_all_location(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    if is_message_startswith(
        message, constants.commands["where_all_command"]["command"]
    ):
        locations_with_people = get_locations_with_people(chat_id)
        reply = ""
        for location_name, users in locations_with_people.items():
            name_list = [f"\t{user.first_name} {user.last_name}" for user in users]
            list_of_ppl_in_location = "\n".join(name_list)
            reply = reply + f"<b>{location_name}</b>\n{list_of_ppl_in_location}\n\n"
        return reply
    return None


async def help(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_startswith(message, constants.commands["help_command"]["command"]):
        return constants.help_message
    return None


async def chat_title(msg: dict) -> tuple[str, dict] | None:
    message = msg.get("text", "")
    chat_id = msg["chat"]["id"]
    if is_message_startswith(message, *constants.change_title_prefixes):
        return "set_chat_title", {"chat_id": chat_id, "text": message}
    return None


async def new_chat_member(msg: dict) -> tuple[str, dict] | None:
    new_chat_member = msg.get("new_chat_member", "")
    if new_chat_member:
        message_id = msg["message_id"]
        chat_id = msg["chat"]["id"]
        return "send_sticker", {
            "chat_id": chat_id,
            "sticker_id": constants.greeting_sticker,
            "reply_to_message_id": message_id,
        }
    return None


async def ping(msg: dict) -> str | None:
    """any tags - location included"""
    message = msg.get("text", "").lower()
    tags_in_message = extract_tags(message)
    if not tags_in_message:
        return None
    chat_id = msg["chat"]["id"]
    template = '<a href="tg://user?id={}">{}</a>'
    valid_tags, invalid_tags = tags.validate_tags(tags_in_message)
    response = ""
    if valid_tags:
        users = tags.fetch_users_with_tags(chat_id, valid_tags)
        response += (
            ", ".join(
                [
                    template.format(user.user_id, user.username or user.first_name)
                    for user in users
                ]
            )
            + "\n"
        )
    if invalid_tags:
        response += (
            "These tags do not exist, create them via /create_tag command or check the list via /all_tags command: \n"
            + ", ".join(invalid_tags)
        )
    return response


async def add_tag(msg: dict) -> str | None:
    message = msg.get("text", "")

    if is_message_startswith(message, constants.commands["add_tag"]["command"]):
        command_args = message.split(maxsplit=2)
        if len(command_args) >= 2:
            tags_to_add = extract_words(command_args[1])
            valid_tags, invalid_tags = tags.validate_tags(tags_to_add)
            response = ""
            if valid_tags:
                chat_id = msg["chat"]["id"]
                user_id = msg["from"]["id"]
                tags.add_tags(chat_id, user_id, valid_tags)
                response = f"Tags added - {', '.join(valid_tags)}"
            if invalid_tags:
                response += (
                    "These tags do not exist, create them via /create_tag command or check the list via /all_tags command: \n"
                    + ", ".join(invalid_tags)
                )
            return response
        return "No tags specified, create a tag via /create_tag command or check the list via /all_tags command."
    return None


async def create_tag(msg: dict) -> str | None:
    message = msg.get("text", "")

    if is_message_startswith(message, constants.commands["create_tag"]["command"]):
        command_args = message.split(maxsplit=2)
        if len(command_args) >= 2:
            
        return "No tag specified."
