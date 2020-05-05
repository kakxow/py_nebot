import httpx


dog_urls = {
  'corgi': "https://dog.ceo/api/breed/corgi/cardigan/images/random",
  'toy': "https://dog.ceo/api/breed/terrier/toy/images/random",
  'pug': "https://dog.ceo/api/breed/pug/images/random",
  'shiba': "http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=false",
  'random': "https://dog.ceo/api/breeds/image/random",
}


async def get_dog(dog: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(dog_urls[dog])
        data = response.json()
    if dog == "shiba":
        return data[0]
    else:
        return data['message']
