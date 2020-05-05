from .constants import greeting_sticker
from . import triggers


async def on_message(bot, msg: dict):
    _chat = msg.get('chat', {})
    chat_id = _chat.get('id', '')

    new_chat_member = msg.get('new_chat_member', '')
    if new_chat_member:
        message_id = msg.get('message_id', '')
        await bot.send_sticker(
            chat_id, greeting_sticker,
            reply_to_message_id=message_id
        )
        return

    text = msg.get('text', '')
    if not text:
        return
    if 'ето не чат' in text:
        await bot.set_chat_title(chat_id, text)
        return
    for _, trigger in triggers.__dict__.items():
        message = await trigger(text.lower())
        if message:
            await bot.send_message(chat_id, message)
            return
