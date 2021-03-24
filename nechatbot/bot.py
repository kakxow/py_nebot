import asyncio
import json
from urllib.parse import urljoin, quote

import aiofiles  # type: ignore
import httpx  # type: ignore

from .calendar import check_birthdays
from .constants import TG_API_URL


filename = "last_update_id.txt"


class Bot:
    def __init__(self, token: str) -> None:
        self.client = httpx.AsyncClient(base_url=TG_API_URL)
        self.token = token
        try:
            with open(filename, mode="r") as f:
                self.last_update_id = int(f.read())
        except FileNotFoundError:
            self.last_update_id = 0
        print("bot initialized")

    async def start(self) -> None:
        print("bot started")
        while True:
            await check_birthdays(self)
            updates = await self.poll()
            for update in updates:
                asyncio.ensure_future(self.on_message(update.get("message", {})))
            await asyncio.sleep(0.3)

    async def send_sticker(self, chat_id: str, sticker_id: str, **kwargs) -> None:
        data = {"sticker": sticker_id, "chat_id": chat_id, **kwargs}
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/sendSticker"))
        await self.client.post(url, json=data)

    async def send_message(self, chat_id, text, **kwargs) -> None:
        print("Message to send - ", text)
        data = {"text": text, "chat_id": chat_id, "parse_mode": "HTML", **kwargs}
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/sendMessage"))
        response = await self.client.post(url, json=data)
        return json.loads(response.text)["result"]

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
        params = {"offset": self.last_update_id}
        try:
            response = await self.client.get(url=url, params=params, timeout=0.5)
        except httpx._exceptions.HTTPError:
            updates = []
        else:
            updates = json.loads(response.text)["result"]
        if updates:
            print(len(updates), " updates received.")
            last_update = max(updates, key=lambda x: x["update_id"])
            self.last_update_id = last_update["update_id"] + 1
            async with aiofiles.open(filename, mode="w") as f:
                await f.write(str(self.last_update_id))
        return updates

    async def delete_message(self, chat_id: int, message_id: int) -> None:
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/deleteMessage"))
        data = {"chat_id": chat_id, "message_id": message_id}
        await self.client.post(url, json=data)

    async def on_message(self, msg: dict):
        raise NotImplementedError
