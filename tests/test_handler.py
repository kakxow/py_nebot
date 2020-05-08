import asyncio
from unittest.mock import ANY

import asynctest  # type: ignore
import pytest  # type: ignore

from nechatbot import handler


@pytest.fixture
def mocked_bot():
    bot = asynctest.CoroutineMock()

    bot.send_sticker.return_value = asyncio.Future()
    bot.send_sticker.return_value.set_result(None)

    bot.set_chat_title.return_value = asyncio.Future()
    bot.set_chat_title.return_value.set_result(None)

    bot.send_message.return_value = asyncio.Future()
    bot.send_message.return_value.set_result(None)

    return bot


@pytest.mark.asyncio
async def test_handler_new_chat_member(mocked_bot):
    msg = {
        "chat": {"id": "test_chat_id"},
        "new_chat_member": "test_member",
        "message_id": "test_message_id",
    }
    await handler.on_message(mocked_bot, msg)
    mocked_bot.send_sticker.assert_called_once_with(
        "test_chat_id",
        ANY,
        reply_to_message_id="test_message_id"
    )
    mocked_bot.set_chat_title.assert_not_called()
    mocked_bot.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_handler_set_chat_title(mocked_bot):
    msg = {
        "chat": {"id": "test_chat_id"},
        "message_id": "test_message_id",
        "text": "ето не чат с Даришкой",
    }
    await handler.on_message(mocked_bot, msg)
    mocked_bot.set_chat_title.assert_called_once_with(
        "test_chat_id",
        "ето не чат с Даришкой"
    )
    mocked_bot.send_sticker.assert_not_called()
    mocked_bot.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_handler_send_message(mocked_bot):
    msg = {
        "chat": {"id": "test_chat_id"},
        "message_id": "test_message_id",
        "text": "триста",
    }
    await handler.on_message(mocked_bot, msg)
    mocked_bot.send_message.assert_called_once_with(
        "test_chat_id",
        ANY
    )
    mocked_bot.set_chat_title.assert_not_called()
    mocked_bot.send_sticker.assert_not_called()


@pytest.mark.asyncio
async def test_handler_no_text(mocked_bot):
    msg = {
        "chat": {"id": "test_chat_id"},
        "message_id": "test_message_id",
    }
    await handler.on_message(mocked_bot, msg)
    mocked_bot.send_message.assert_not_called()
    mocked_bot.set_chat_title.assert_not_called()
    mocked_bot.send_sticker.assert_not_called()


@pytest.mark.asyncio
async def test_handler_no_triggers(mocked_bot):
    msg = {
        "chat": {"id": "test_chat_id"},
        "message_id": "test_message_id",
        "text": "abracadabra",
    }
    await handler.on_message(mocked_bot, msg)
    mocked_bot.send_message.assert_not_called()
    mocked_bot.set_chat_title.assert_not_called()
    mocked_bot.send_sticker.assert_not_called()
