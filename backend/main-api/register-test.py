import requests

URL = "http://localhost:3000/auth/register"  # замени на свой адрес сервера, если нужно

payload = {
    "email": "newuser@example.com",
    "password": "mypass123",
    "role": "user",
    # "team_id": "uuid_существующей_команды" # если нужно сразу добавить к команде
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(URL, json=payload, headers=headers)

print("Status code:", response.status_code)
print("Response body:", response.json())