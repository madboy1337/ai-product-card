from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os

from app.schemas import ProductInput, ProductCardOutput
from app.prompts import SYSTEM_PROMPT, build_user_prompt
from app.llm_client import generate_product_card
from app.utils import validate_and_clean

load_dotenv()

app = FastAPI(title="AI Product Card Generator", version="1.0")

@app.post("/generate", response_model=ProductCardOutput)
async def generate_card(product: ProductInput):
    data, missing = validate_and_clean(product)

    if data.get("_no_data"):
        return ProductCardOutput(
            seo_title=f"{product.name} — {product.manufacturer}"[:70],
            seo_description="данных нет: недостаточно информации для формирования описания",
            key_specs={"характеристики": "данных нет"},
            search_queries=[f"{product.name} купить", f"{product.manufacturer} {product.name}"],
            commercial_block="данных нет: недостаточно информации",
            missing_fields=missing,
        )

    user_prompt = build_user_prompt(data)
    try:
        result = generate_product_card(SYSTEM_PROMPT, user_prompt)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Ошибка при разборе ответа от LLM: {e}")

    if missing and not result.missing_fields:
        result.missing_fields = missing

    return result