import requests

URL = "http://localhost:4000/api/chat"

payload = {
    "messages": [
        {"role": "user", "content": "Привет! Что ты умеешь?"}
    ]
}

headers = {
    "Content-Type": "application/json"
}

def main():
    response = requests.post(URL, json=payload, headers=headers)
    print("Status:", response.status_code)
    try:
        print("Response:", response.json())
    except Exception:
        print("Raw response:", response.text)

if __name__ == "__main__":
    main()