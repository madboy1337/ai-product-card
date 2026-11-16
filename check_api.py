import os
import requests
from dotenv import load_dotenv

# Загружаем ключи из .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("OPENAI_MODEL")

# Собираем полный адрес (добавляем /chat/completions)
url = f"{base_url}/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": model,
    "messages": [{"role": "user", "content": "Hello"}]
}

print(f"Отправляем запрос на {url}...")
try:
    response = requests.post(url, headers=headers, json=data, timeout=120)
    print(f"Код ответа: {response.status_code}")
    print(response.text)
except Exception as e:
    print(f"Ошибка сети: {e}")
    