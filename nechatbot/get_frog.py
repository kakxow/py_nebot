import re

import httpx  # type: ignore


frog_img_pattern = r"<img class=\"lazy thumbnail aspect-wide-contain\" .* data-src=\"(.*?)\""


async def get(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        text = response.text
        print("response = ", response)
    match = re.search(frog_img_pattern, text, re.M)
    print("match = ", match)
    if match:
        return match.group(1)
    else:
        return ""
