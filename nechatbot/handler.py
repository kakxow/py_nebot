import asyncio

from . import triggers, inline_commands
from .constants import greeting_sticker, change_title_prefixes, report_message_delete_delay
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
            reply = await callable_trigger(msg)
            if reply:
                if isinstance(reply, tuple):
                    message, kwargs = reply
                    sent_message = await bot.send_message(chat_id, message, **kwargs)
                else:
                    message = reply
                sent_message = await bot.send_message(chat_id, message)
                if trigger_name in triggers.auto_delete_list:
                    await asyncio.sleep(report_message_delete_delay)
                    await bot.delete_message(chat_id, sent_message["message_id"])


async def on_inline_query(bot, inline_query):
    for trigger_name in inline_commands.__all__:
        inline_command = getattr(inline_commands, trigger_name)
        inline_query_results = await inline_command(inline_query)
        if inline_query_results:
            await bot.answer_inline_query(inline_query["id"], inline_query_results)
