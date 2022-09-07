import asyncio
import json
import logging

import aiofiles  # type: ignore
import httpx  # type: ignore

from .constants import BASE_URL, POLL_TIMEOUT, commands, WEBHOOK_URL, SECURITY_KEY


filename = "last_update_id.txt"


class Bot:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.client = httpx.AsyncClient(base_url=BASE_URL)
        self.timeout = POLL_TIMEOUT
        self.token = token
        try:
            with open(filename, mode="r") as f:
                self.last_update_id = int(f.read())
        except FileNotFoundError:
            self.last_update_id = 0
        self.logger.info("bot initialized")

        asyncio.get_event_loop().run_until_complete(self.set_my_commands())
        asyncio.get_event_loop().run_until_complete(self.delete_webhook())
        asyncio.get_event_loop().run_until_complete(self.set_webhook())

    async def start(self) -> None:
        self.logger.info("bot started")
        while True:
            updates = await self.poll()
            for update in updates:
                self.dispatch_update(update)

    async def dispatch_update(self, update):
        self.logger.debug("%s", update)
        if update.get("inline_query", {}):
            asyncio.ensure_future(self.on_inline_query(update.get("inline_query", {})))
        else:
            asyncio.ensure_future(self.on_message(update.get("message", {})))

        url = "/setWebhook"
        data = {"url": webhook_url, "secret_token": SECURITY_KEY}
        await self.client.post(url, json=data)

    async def delete_webhook(self):
        url = "/deleteWebhook"
        await self.client.post(url)

        url = "/sendSticker"
        data = {"sticker": sticker_id, "chat_id": chat_id, **kwargs}
        await self.client.post(url, json=data)

        url = "/sendMessage"
        self.logger.debug("Message to send - %s", text)
        data = {"text": text, "chat_id": chat_id, "parse_mode": "HTML", **kwargs}
        response = await self.client.post(url, json=data)
        return json.loads(response.text)["result"]

        url = "/setChatTitle"
        data = {"title": text, "chat_id": chat_id}
        await self.client.post(url, json=data)

        url = "/getChatMember"
        data = {"chat_id": chat_id, "user_id": user_id}
        response = await self.client.post(url, json=data)
        if response.is_error:
            return {}
        return json.loads(response.text)["result"]

    async def poll(self) -> list:
        url = "/getUpdates"
        params = {"offset": self.last_update_id, "timeout": self.timeout}
        try:
            response = await self.client.get(
                url=url, params=params, timeout=self.timeout
            )
        except httpx._exceptions.HTTPError:
            updates = []
        else:
            updates = json.loads(response.text)["result"]
        if updates:
            self.logger.debug("%s updates received.", len(updates))
            last_update = max(updates, key=lambda x: x["update_id"])
            self.last_update_id = last_update["update_id"] + 1
            async with aiofiles.open(filename, mode="w") as f:
                await f.write(str(self.last_update_id))
        return updates

    async def delete_message(self, chat_id: int, message_id: int) -> None:
        url = "/deleteMessage"
        data = {"chat_id": chat_id, "message_id": message_id}
        await self.client.post(url, json=data)

    async def answer_inline_query(self, inline_query_id: str, results: list):
        url = "/answerInlineQuery"
        data = {"inline_query_id": inline_query_id, "results": results}
        await self.client.post(url, json=data)

    async def set_my_commands(self):
        url = "/setMyCommands"
        data = {"commands": list(commands.values())}
        await self.client.post(url, json=data)

    async def pin_chat_message(self, chat_id: str, message_id: int):
        url = "/pinChatMessage"
        data = {"chat_id": chat_id, "message_id": message_id}
        await self.client.post(url, json=data)

    async def unpin_chat_message(self, chat_id: str, message_id: int):
        url = "/unpinChatMessage"
        data = {"chat_id": chat_id, "message_id": message_id}
        await self.client.post(url, json=data)

    async def edit_message_text(
        self, chat_id: str, message_id: int, text: str, reply_markup
    ):
        url = "/editMessageText"
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "reply_markup": reply_markup,
        }
        await self.client.post(url, json=data)

    async def on_message(self, msg: dict):
        raise NotImplementedError

    async def on_inline_query(self, inline_query: dict):
        raise NotImplementedError
