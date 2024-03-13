import re

import httpx  # type: ignore


frog_img_pattern = r"https://cdn-0.generatormix.com/images/frog/.*?\.jpg"


async def get(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        text = response.text
    match = re.search(frog_img_pattern, text, re.M)
    if match:
        return match.group(0)
    else:
        return ""
