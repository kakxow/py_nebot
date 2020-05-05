import random
import re

from .constants import net, greeting_sticker, triggers


async def on_message(bot, msg: dict):
    message_id = msg.get('message_id', '')
    chat = msg.get('chat', {})
    text: str = msg.get('text', '')
    new_chat_member = msg.get('new_chat_member', '')
    chat_id = chat.get('id', '')
    if new_chat_member:
        await bot.send_sticker(chat_id, greeting_sticker, reply_to_message_id=message_id)
    elif text:
        if 'ето не чат' in text:
            await bot.set_chat_title(chat_id, text)
        if text.lower().endswith('нет'):
            await bot.send_message(chat_id, random.choice(net))
        for (variants, result) in triggers:
            if re.search('|'.join(variants), text, re.I):
                message = await result()
                await bot.send_message(chat_id, message)
