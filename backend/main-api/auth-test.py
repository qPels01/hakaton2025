import requests

# Базовый URL вашего API
BASE_URL = 'http://localhost:3000/api'

# Данные для регистрации
register_data = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "password123",
    "company_name": "Test Company",
    "is_admin": False
}

# Данные для авторизации
login_data = {
    "username": "testuser",
    "password": "password123"
}

# Тестовый запрос для проверки миддлвара
protected_url = f"{BASE_URL}/user/protected"

# 1. Регистрация пользователя
response = requests.post(f"{BASE_URL}/auth/register", json=register_data)

if response.status_code == 201:
    print("Регистрация успешна!")
else:
    print(f"Ошибка регистрации: {response.status_code}, {response.json()}")

# 2. Авторизация и получение токена
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

if response.status_code == 200:
    print("Авторизация успешна!")
    token = response.json()['token']
    print(f"Полученный токен: {token}")
else:
    print(f"Ошибка авторизации: {response.status_code}, {response.json()}")

# 3. Проверка защищённого маршрута с токеном
headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(protected_url, headers=headers)

if response.status_code == 200:
    print("Доступ к защищённому маршруту успешен!")
    print(response.json())
else:
    print(f"Ошибка доступа к защищённому маршруту: {response.status_code}, {response.json()}")