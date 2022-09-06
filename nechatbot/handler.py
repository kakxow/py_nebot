import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bot import Bot
from . import triggers, inline_commands
from .constants import report_message_delete_delay


async def on_message(bot: Bot, msg: dict) -> None:
    chat_id = msg["chat"]["id"]

    for trigger_name in triggers.__all__:
        callable_trigger = getattr(triggers, trigger_name)
        match await callable_trigger(msg):
            case (command, data):
                sent_message = await getattr(bot, command)(**data)
            case None | "":
                continue
            case message:
                sent_message = await bot.send_message(chat_id, message)
        if trigger_name in triggers.auto_delete_list:
            await asyncio.sleep(report_message_delete_delay)
            await bot.delete_message(chat_id, sent_message["message_id"])


async def on_inline_query(bot: Bot, inline_query: dict) -> None:
    for trigger_name in inline_commands.__all__:
        inline_command = getattr(inline_commands, trigger_name)
        inline_query_results = await inline_command(inline_query)
        if inline_query_results:
            await bot.answer_inline_query(inline_query["id"], inline_query_results)
