import json

from . import triggers
from .constants import greeting_sticker, change_title_prefixes
from .predicates import is_message_startswith


async def on_message(bot, msg: dict):
    chat = msg.get("chat", {})
    chat_id = chat.get("id", "")

    new_chat_member = msg.get("new_chat_member", "")
    if new_chat_member:
        message_id = msg.get("message_id", "")
        return await bot.send_sticker(
            chat_id, greeting_sticker, reply_to_message_id=message_id
        )

    text = msg.get("text", "")
    # print(json.dumps(msg, indent=4))
    # print(type(chat_id), chat_id)

    if is_message_startswith(text, *change_title_prefixes):
        return await bot.set_chat_title(chat_id, text)

    callable_triggers = (getattr(triggers, trigger) for trigger in triggers.__all__)
    for trigger in callable_triggers:
        message = await trigger(msg)
        if message:
            return await bot.send_message(chat_id, message, parse_mode="HTML")
