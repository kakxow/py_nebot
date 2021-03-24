import json

from . import triggers
from .constants import greeting_sticker, change_title_prefixes
from .predicates import is_message_startswith


async def on_message(bot, msg: dict) -> None:
    chat = msg.get("chat", {})
    chat_id = chat.get("id", "")

    new_chat_member = msg.get("new_chat_member", "")
    if new_chat_member:
        message_id = msg.get("message_id", "")
        return await bot.send_sticker(
            chat_id, greeting_sticker, reply_to_message_id=message_id
        )

    if chat_id:
        text = msg.get("text", "")

        if is_message_startswith(text, *change_title_prefixes):
            return await bot.set_chat_title(chat_id, text)

        for trigger_name in triggers.__all__:
            callable_trigger = getattr(triggers, trigger_name)
            message = await callable_trigger(msg)
            if message:
                sent_message = await bot.send_message(chat_id, message)
                if 
                return
