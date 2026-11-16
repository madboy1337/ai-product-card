import requests
import json

url = "http://127.0.0.1:8000/generate"

# Данные для ВТОРОГО товара (с пропусками)
payload = {
    "name": "Датчик давления ДД-100",
    "manufacturer": "ПримерПрибор",
    "specs": {
        "диапазон измерений": "0-10 МПа"
    },
    "description": None
}

print("Отправляем запрос... Подождите, нейросеть думает...")

try:
    response = requests.post(url, json=payload, timeout=120)
    print(f"Код ответа: {response.status_code}")
    
    if response.status_code == 200:
        print("\n=== УСПЕХ! Ответ от нейросети ===")
        result_data = response.json()
        print(json.dumps(result_data, ensure_ascii=False, indent=2))
        
        # СОХРАНЯЕМ В ФАЙЛ
        filepath = "examples/result_2.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        print(f"\n[+] Результат успешно сохранен в файл: {filepath}")
        
    else:
        print("\n=== ОШИБКА ===")
        print(response.text)

except Exception as e:
    print(f"\n=== ОШИБКА ПОДКЛЮЧЕНИЯ ===\n{e}")