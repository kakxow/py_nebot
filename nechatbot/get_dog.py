import httpx


async def get(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
    if "shibe" in url:
        return data[0]
    else:
        return data['message']
