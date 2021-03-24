import asyncio


async def delete_message_delayed(bot, chat_id: int, message_id: int, delay: int) -> None:
    await asyncio.sleep(delay)
    await bot.delete_message(chat_id, message_id)
