import asyncio
import json
from urllib.parse import urljoin, quote

import aiofiles  # type: ignore
import httpx  # type: ignore

from .constants import TG_API_URL


filename = "last_update_id.txt"


class Bot:
    def __init__(self, token: str):
        self.client = httpx.AsyncClient(base_url=TG_API_URL)
        self.token = token
        try:
            with open(filename, mode="r") as f:
                self.last_update_id = int(f.read())
        except FileNotFoundError:
            self.last_update_id = 0
        print("bot initialized")

    async def start(self):
        print("bot started")
        while True:
            updates = await self.poll()
            for update in updates:
                await self.on_message(update.get("message", {}))
            await asyncio.sleep(0.3)

    async def send_sticker(self, chat_id: str, sticker_id: str, **kwargs):
        data = {"sticker": sticker_id, "chat_id": chat_id, **kwargs}
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/sendSticker"))
        await self.client.post(url, json=data)

    async def send_message(self, chat_id, text, **kwargs):
        print("Message to send - ", text)
        data = {"text": text, "chat_id": chat_id, **kwargs}
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/sendMessage"))
        await self.client.post(url, json=data)

    async def set_chat_title(self, chat_id: str, text: str):
        data = {"title": text, "chat_id": chat_id}
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/setChatTitle"))
        response = await self.client.post(url, json=data)
        return response

    async def get_chat_member(self, chat_id: str, user_id: int) -> dict:
        data = {"chat_id": chat_id, "user_id": user_id}
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/getChatMember"))
        response = await self.client.post(url, json=data)
        return json.loads(response.text)["result"]

    async def poll(self):
        url = urljoin(TG_API_URL, quote(f"bot{self.token}/getUpdates"))
        params = {"offset": self.last_update_id}
        response = await self.client.get(url=url, params=params)
        updates = json.loads(response.text)["result"]
        if updates:
            print(len(updates), " updates received.")
            last_update = max(updates, key=lambda x: x["update_id"])
            self.last_update_id = last_update["update_id"] + 1
            async with aiofiles.open(filename, mode="w") as f:
                await f.write(str(self.last_update_id))
        return updates
    
    async def congrats_today_birthdays(self) -> Optional[str]:
    ids = social_credit_calc.get_today_birthdays()
    if ids:
        chat_id = int(msg.get("chat", {}).get("id", ""))
        chat_members = [await bot.get_chat_member(chat_id, int(id)) for id in ids]
        usernames = [f'@{chat_member.get("user").get("username", "")}' for chat_member in chat_members]
        text_usernames = ", ".join(usernames)
        return f"Happy birthday {text_usernames}!"
    return None

    async def on_message(self, msg: dict):
        raise NotImplementedError
