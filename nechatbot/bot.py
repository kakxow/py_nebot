import asyncio
import json
from urllib.parse import urljoin, quote

import aiofiles
import httpx

from .constants import TG_API_URL


filename = 'last_update_id.txt'


class Bot:
    def __init__(self, token: str):
        self.client = httpx.AsyncClient(base_url=TG_API_URL)
        self.token = token
        try:
            with open(filename, mode='r') as f:
                self.last_update_id = int(f.read())
        except FileNotFoundError:
            self.last_update_id = 0

    async def start(self):
        while True:
            updates = await self.poll()
            for update in updates:
                await self.on_message(update['message'])
            await asyncio.sleep(0.3)

    async def send_sticker(self, chat_id: str, sticker_id: str, **kwargs):
        data = {'sticker': sticker_id, 'chat_id': chat_id, **kwargs}
        url = urljoin(TG_API_URL, quote(f'bot{self.token}/sendSticker'))
        await self.client.post(url, json=data)

    async def send_message(self, chat_id, text, **kwargs):
        data = {'text': text, 'chat_id': chat_id, **kwargs}
        url = urljoin(TG_API_URL, quote(f'bot{self.token}/sendMessage'))
        await self.client.post(url, json=data)

    async def set_chat_title(self, chat_id: str, text: str):
        data = {'title': text, 'chat_id': chat_id}
        url = urljoin(TG_API_URL, quote(f'bot{self.token}/setChatTitle'))
        response = await self.client.post(url, json=data)
        return response

    async def poll(self):
        url = urljoin(TG_API_URL, quote(f'bot{self.token}/getUpdates'))
        params = {'offset': self.last_update_id}
        response = await self.client.get(url=url, params=params)
        updates = json.loads(response.text)['result']
        if updates:
            last_update = max(updates, key=lambda x: x['update_id'])
            self.last_update_id = last_update['update_id'] + 1
            async with aiofiles.open(filename, mode='w') as f:
                await f.write(str(self.last_update_id))
        return updates

    async def on_message(self, msg: dict):
        raise NotImplementedError
