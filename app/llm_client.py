import os
from openai import OpenAI, APIError, APITimeoutError
from app.schemas import ProductCardOutput

def generate_product_card(system_prompt: str, user_prompt: str) -> ProductCardOutput:
    # Читаем настройки прямо перед запросом, когда .env уже точно загружен
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        raise RuntimeError("Ключ OPENAI_API_KEY не найден. Проверьте файл .env")

    # Инициализируем клиент внутри функции
    client = OpenAI(
        api_key=api_key,
        base_url=base_url if base_url else None
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
        )
        json_content = response.choices[0].message.content
        # Убираем возможные маркеры разметки markdown
        json_content = json_content.replace("```json", "").replace("```", "").strip()
        return ProductCardOutput.model_validate_json(json_content)
    except APITimeoutError:
        raise RuntimeError("LLM API timeout — попробуйте позже")
    except APIError as e:
        raise RuntimeError(f"Ошибка LLM API: {e}")