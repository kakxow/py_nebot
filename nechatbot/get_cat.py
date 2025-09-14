import httpx  # type: ignore


async def get(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
    if isinstance(data, dict):
        return data["url"]  # type: ignore
    elif isinstance(data, list):
        return data[0]["url"]  # type: ignore
    return ""
