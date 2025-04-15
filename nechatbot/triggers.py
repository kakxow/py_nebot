import random
import re

from .location import (
    change_location,
    get_people_from_location,
    get_locations_with_people,
    locations,
    locations_text,
)
from . import constants, get_dog, get_frog, calendar, tags
from .predicates import (
    extract_mentions,
    is_message_contains_words,
    is_message_contains_words_and_emojis,
    is_message_ends_with_word,
    is_message_contains_phrases,
    is_message_startswith,
    is_date,
)


__all__ = [
    "ukraine",
    "roll",
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
    # "net",
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
    "list_tags",
    "assign_tags",
    "free_tags",
    "free_all_tags",
    "create_tag",
    "tagger",
    "your_tags",
    "update_tag",
    "create_location",
    "delete_tag",
]
auto_delete_list = [
    # "where_all_location",
    # "help",
]


async def roll(msg: dict) -> str | None:
    message: str = msg.get("text", "").lower()
    if message.startswith("/roll"):
        _cmd, *args = message.split()
        roll_arg = args[0] if args else "20"
        if roll_arg.isnumeric():
            roll_arg = "d" + roll_arg
        match = re.match(r"(\d*)\s*d(\d+)", roll_arg)
        if not match:
            return f"Invalid argument format {message}, examples - /roll 9d30, /roll d10, /roll 4"
        dice_num, dice_size = match.groups()
        if not dice_num:
            dice_num = 1
        dice_num = int(dice_num)
        dice_size = int(dice_size)
        if not dice_size or not dice_num:
            return f"Arguments should be greater than 0, {message}"
        roll_result = sum(random.choices(range(1, dice_size + 1), k=dice_num))  # noqa: S311
        user = msg["from"]
        first_name = user["first_name"]  # required field
        username = user.get("username", first_name)
        dices = "a" if dice_num == 1 else f"{dice_num} x"
        return f"{username} rolled a {roll_result} with {dices} 🎲 {dice_size}"
    return None


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
    shibe_url = "https://dog.ceo/api/breed/shiba/images/random"
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
                "chat_id": chat_id,
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


async def ping_location2(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    template = '<a href="tg://user?id={}">{}</a>'
    for loc in locations:
        if is_message_contains_phrases(message, *loc.mention_tags):
            users = get_people_from_location(chat_id, loc.name)
            return ", ".join(
                [
                    template.format(user.id, user.username or user.first_name)
                    for user in users
                ]
            )
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
        if not reply:
            reply = "No locations set."
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


async def list_tags(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_startswith(message, constants.commands["list_tags"]["command"]):
        reply = ""
        for tag, mentions in tags.list_tags().items():
            list_of_mentions = ", ".join(
                [mention.name for mention in mentions]
            ).replace("@", "")
            reply = reply + f"<b>{tag}</b>\t{list_of_mentions}\n\n"
        if not reply:
            reply = "No custom tags found."
        return reply
    return None


async def assign_tags(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_startswith(message, constants.commands["assign_tags"]["command"]):
        tags_from_command = message.split()[1:]
        if not tags_from_command:
            return "Run command with a tag name or names (separated by space) as an argument. Example: /assign_tags queer autist"
        return tags.assign_tags(msg["from"], msg["chat"]["id"], tags_from_command)
    return None


async def create_tag(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_startswith(message, constants.commands["create_tag"]["command"]):
        arguments = message.split()[1:]
        if len(arguments) < 2:
            return "Run this command with a name and a list of mentions as arguments, separated by space. Example: /create_tag anime nya kawaii"
        tag_name, *mentions = arguments
        return tags.create_tag(tag_name, mentions)
    return None


async def create_location(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_startswith(message, constants.commands["create_location"]["command"]):
        arguments = message.split()[1:]
        if len(arguments) < 2:
            return "Run this command with a location name and a list of mentions as arguments, separated by space. Example: /create_location anime nya kawaii"
        tag_name, *mentions = arguments
        return tags.create_tag(tag_name, mentions, group="location")
    return None


async def free_tags(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_startswith(message, constants.commands["free_tags"]["command"]):
        tag_list = message.split()[1:]
        if len(tag_list) < 1:
            return "Run this command with a list of tag names as arguments, separated by space. Example: /free_tags anime freebsd"
        return tags.free_tags(msg["from"], msg["chat"]["id"], tag_list)
    return None


async def free_all_tags(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_startswith(message, constants.commands["free_all_tags"]["command"]):
        return tags.free_all_tags(msg["from"], msg["chat"]["id"])
    return None


async def update_tag(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_startswith(message, constants.commands["update_tag"]["command"]):
        arguments = message.split()[1:]
        if len(arguments) < 2:
            return "Run this command with a name and a list of new mentions as arguments, separated by space. Example: /update_tag anime nya kawaii"
        tag_name, *mentions = arguments
        return tags.update_tag(tag_name, mentions)
    return None


async def your_tags(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    if is_message_startswith(message, constants.commands["your_tags"]["command"]):
        return tags.your_tags(msg["from"], msg["chat"]["id"])
    return None


async def tagger(msg: dict) -> str | None:
    message = msg.get("text", "").lower()
    chat_id = msg["chat"]["id"]
    template = '<a href="tg://user?id={}">{}</a>'
    mentions = extract_mentions(message)
    if mentions:
        users = tags.tagger(chat_id, list(mentions))
        return ", ".join(
            [
                template.format(user.id, user.username or user.first_name)
                for user in users
            ]
        )
    return None


async def delete_tag(msg: dict) -> str | None:
    message = msg.get("text", "")
    if is_message_startswith(message, "/delete_tag_please"):
        arguments = message.split()[1:]
        if len(arguments) < 1:
            return "Run this command with a name of a tag. Example: /delete_tag_please anime"
        tag_name = arguments[0]
        return tags.delete_tag(tag_name)
    return None
