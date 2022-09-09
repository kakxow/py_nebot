import asyncio
import json
import logging

import httpx

from .constants import BASE_URL, POLL_TIMEOUT, commands, WEBHOOK_URL, SECURITY_KEY

KwargsType = dict[str, str | int | bool]


class Bot:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.client = httpx.AsyncClient(base_url=BASE_URL)
        self.timeout = POLL_TIMEOUT
        self.last_update_id = 0
        self.logger.info("bot initialized")

        asyncio.get_event_loop().run_until_complete(self.set_my_commands())
        asyncio.get_event_loop().run_until_complete(self.set_webhook())

    async def start(self) -> None:
        """use for longpolling method"""
        await self.delete_webhook()
        self.logger.info("bot started")
        while True:
            updates = await self.poll()
            for update in updates:
                await self.dispatch_update(update)

    async def dispatch_update(self, update: dict) -> None:
        self.logger.debug("%s", update)
        match update:
            case {"inline_query": inline_query}:
                method = self.on_inline_query(inline_query)
            case {"message": message}:
                method = self.on_message(message)
            case _:
                return None
        asyncio.ensure_future(method)

    async def set_webhook(self, webhook_url: str = WEBHOOK_URL) -> None:
        url = "/setWebhook"
        data = {"url": webhook_url, "secret_token": SECURITY_KEY}
        await self.client.post(url, json=data)

    async def delete_webhook(self) -> None:
        url = "/deleteWebhook"
        await self.client.post(url)

    async def send_sticker(
        self, chat_id: int, sticker_id: str, **kwargs: KwargsType
    ) -> None:
        url = "/sendSticker"
        data = {"sticker": sticker_id, "chat_id": chat_id, **kwargs}
        await self.client.post(url, json=data)

    async def send_message(self, chat_id: int, text: str, **kwargs: KwargsType) -> dict:
        url = "/sendMessage"
        self.logger.debug("Message to send - %s", text)
        data = {"text": text, "chat_id": chat_id, "parse_mode": "HTML", **kwargs}
        response = await self.client.post(url, json=data)
        return json.loads(response.text)["result"]

    async def set_chat_title(self, chat_id: int, text: str) -> None:
        url = "/setChatTitle"
        data = {"title": text, "chat_id": chat_id}
        await self.client.post(url, json=data)

    async def get_chat_member(self, chat_id: int, user_id: int) -> dict:
        url = "/getChatMember"
        data = {"chat_id": chat_id, "user_id": user_id}
        response = await self.client.post(url, json=data)
        if response.is_error:
            return {}
        return json.loads(response.text)["result"]

    async def poll(self) -> list[dict]:
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
        return updates

    async def delete_message(self, chat_id: int, message_id: int) -> None:
        url = "/deleteMessage"
        data = {"chat_id": chat_id, "message_id": message_id}
        await self.client.post(url, json=data)

    async def answer_inline_query(self, inline_query_id: str, results: list) -> None:
        url = "/answerInlineQuery"
        data = {"inline_query_id": inline_query_id, "results": results}
        await self.client.post(url, json=data)

    async def set_my_commands(self) -> None:
        url = "/setMyCommands"
        data = {"commands": list(commands.values())}
        await self.client.post(url, json=data)

    async def pin_chat_message(self, chat_id: int, message_id: int) -> None:
        url = "/pinChatMessage"
        data = {"chat_id": chat_id, "message_id": message_id}
        await self.client.post(url, json=data)

    async def unpin_chat_message(self, chat_id: int, message_id: int) -> None:
        url = "/unpinChatMessage"
        data = {"chat_id": chat_id, "message_id": message_id}
        await self.client.post(url, json=data)

    async def edit_message_text(
        self, chat_id: int, message_id: int, text: str, **kwargs: KwargsType
    ) -> None:
        url = "/editMessageText"
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            **kwargs,
        }
        await self.client.post(url, json=data)

    async def on_message(self, _msg: dict) -> None:
        raise NotImplementedError

    async def on_inline_query(self, _inline_query: dict) -> None:
        raise NotImplementedError
