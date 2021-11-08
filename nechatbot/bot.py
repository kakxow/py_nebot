import asyncio
import json
import logging
import threading
from types import MethodType
from urllib.parse import urljoin, quote

import aiofiles  # type: ignore
import httpx  # type: ignore

from .calendar import check_birthdays
from .constants import TG_API_URL, POLL_TIMEOUT


filename = "last_update_id.txt"


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Bot:
    def __init__(self, token: str, on_message, on_inline_query) -> None:
        self.on_message = MethodType(on_message, self)
        self.on_inline_query = MethodType(on_inline_query, self)
        self.logger = logging.getLogger(__name__)
        self.client = httpx.AsyncClient(base_url=TG_API_URL)
        self.timeout = POLL_TIMEOUT
        self.token = token
        try:
            with open(filename, mode="r") as f:
                self.last_update_id = int(f.read())
        except FileNotFoundError:
            self.last_update_id = 0
        self.logger.debug("bot initialized")

    async def start(self) -> None:
        self.logger.debug("bot started")
        await self.delete_webhook()
        while True:
            await check_birthdays(self)
            updates = await self.poll()
            for update in updates:
                self.logger.debug("%s", update)
                if update.get("inline_query", {}):
                    asyncio.ensure_future(
                        self.on_inline_query(update.get("inline_query", {}))
                    )
                else:
                    asyncio.ensure_future(self.on_message(update.get("message", {})))

    async def send_sticker(self, chat_id: str, sticker_id: str, **kwargs) -> None:
        data = {"sticker": sticker_id, "chat_id": chat_id, **kwargs}
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/sendSticker"))
        await self.client.post(url, json=data)

    async def send_message(self, chat_id, text, **kwargs) -> None:
        self.logger.debug("Message to send - %s", text)
        data = {"text": text, "chat_id": chat_id, "parse_mode": "HTML", **kwargs}
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/sendMessage"))
        response = await self.client.post(url, json=data)
        try:
            response.raise_for_status()
        except httpx._exceptions.HTTPStatusError as exc:
            self.logger.debug(f"HTTP Exception for {exc.request.url} - {exc}")
            self.logger.debug(f"Error response - {response.text}")
            return None
        return json.loads(response.text).get("result")

    async def set_chat_title(self, chat_id: str, text: str) -> None:
        data = {"title": text, "chat_id": chat_id}
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/setChatTitle"))
        await self.client.post(url, json=data)

    async def get_chat_member(self, chat_id: str, user_id: int) -> dict:
        data = {"chat_id": chat_id, "user_id": user_id}
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/getChatMember"))
        response = await self.client.post(url, json=data)
        if response.is_error:
            return {}
        return json.loads(response.text)["result"]

    async def poll(self) -> list:
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/getUpdates"))
        params = {"offset": self.last_update_id, "timeout": self.timeout}
        try:
            response = await self.client.get(
                url=url, params=params, timeout=self.timeout
            )
            response.raise_for_status()
        except httpx._exceptions.HTTPStatusError as exc:
            self.logger.debug(f"HTTP Exception for {exc.request.url} - {exc}")
            self.logger.debug(f"Error response - {response.text}")
            updates = []
        except httpx._exceptions.HTTPError:
            updates = []
        else:
            updates = json.loads(response.text).get("result", [])
        if updates:
            self.logger.debug("%s updates received.", len(updates))
            last_update = max(updates, key=lambda x: x["update_id"])
            self.last_update_id = last_update["update_id"] + 1
            async with aiofiles.open(filename, mode="w") as f:
                await f.write(str(self.last_update_id))
        return updates

    async def delete_message(self, chat_id: int, message_id: int) -> None:
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/deleteMessage"))
        data = {"chat_id": chat_id, "message_id": message_id}
        await self.client.post(url, json=data)

    async def answer_inline_query(self, inline_query_id: str, results: list):
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/answerInlineQuery"))
        data = {"inline_query_id": inline_query_id, "results": results}
        await self.client.post(url, json=data)

    async def delete_webhook(self):
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/deleteWebhook"))
        res = await self.client.get(url)
        self.logger.debug("Webhook disabled. %s", res.text)
