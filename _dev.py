import requests

url = "https://json.extendsclass.com/bin"

api_key = "dd65bf69-573e-11ec-b95c-0242ac110002"
security_key = "CoqLa67o6TZ0sAgfo2YEVdStMSu0RSbM"
headers = {"Api-key": api_key, "Security-key": security_key, "Private": "true"}

json_id = "a73c830e9b5f"

data = [{"user_id1": {"location": "x", "credit": 20, "bday": "25.08.1999"}}]


response1 = requests.put(f"{url}/{json_id}", headers=headers, json=data)
response2 = requests.get(f"{url}/{json_id}", headers=headers)
