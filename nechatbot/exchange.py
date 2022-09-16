import httpx

url_get = 'https://api.exchangerate.host/'
url_convert = 'https://api.exchangerate.host/convert?'

currencies = ['EUR', 'GEL', 'RUB', 'AED', 'AMD', 'KZT', 'QAR']

async def get_exchange_rates(currencies, inline_query:dict) -> list:
    if inline_query["chat_type"] in ("group", "supergroup"):
        date = inline_query["query"]
        for currency in currencies:
            async with httpx.AsyncClient() as client:
                response = await client.get(url_get + f'base=USD&amount=1&symbols={currency}')
                rate = [].add(f'{currency}:{response}/n')
        return rate

async def convert_currency(currency1, currency2, amount, inline_query:dict) -> list:
    if inline_query["chat_type"] in ("group", "supergroup"):
        date = inline_query["query"]
        async with httpx.AsyncClient() as client:
            response = await client.get(url_convert + f'from={currency1}&to={currency2}&amount={amount}')
            return response.text