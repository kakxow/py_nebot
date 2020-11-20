from .constants import greeting_sticker
from . import triggers


async def on_message(bot, msg: dict):
    chat = msg.get('chat', {})
    chat_id = chat.get('id', '')

    new_chat_member = msg.get('new_chat_member', '')
    if new_chat_member:
        message_id = msg.get('message_id', '')
        return await bot.send_sticker(
            chat_id, greeting_sticker,
            reply_to_message_id=message_id
        )

    text = msg.get('text', '')
    if not text:
        return
    if 'ето не чат' in text.lower():
        return await bot.set_chat_title(chat_id, text)

    callable_triggers = \
        (getattr(triggers, trigger) for trigger in triggers.__all__)
    for trigger in callable_triggers:
        message = await trigger(text.lower())
        if message:
            return await bot.send_message(chat_id, message)
