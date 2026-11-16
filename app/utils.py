from app.schemas import ProductInput

def validate_and_clean(product: ProductInput) -> tuple[dict, list[str]]:
    """Возвращает очищенные данные и список отсутствующих полей."""
    missing = []
    data = product.model_dump()

    if not product.name.strip():
        missing.append("name")
    if not product.manufacturer.strip():
        missing.append("manufacturer")
    if not product.specs:
        missing.append("specs (характеристики)")
    if not product.description or not product.description.strip():
        missing.append("description (описание)")

    if not product.specs and not product.description:
        data["_no_data"] = True

    return data, missing