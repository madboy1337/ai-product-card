from pydantic import BaseModel, Field
from typing import Dict, Optional

class ProductInput(BaseModel):
    name: str = Field(..., description="Название товара")
    manufacturer: str = Field(..., description="Производитель")
    specs: Dict[str, str] = Field(
        default_factory=dict,
        description="Краткие характеристики"
    )
    description: Optional[str] = Field(
        None,
        description="Текстовое описание"
    )

class ProductCardOutput(BaseModel):
    seo_title: str = Field(..., max_length=70)
    seo_description: str = Field(..., min_length=800, max_length=1200)
    key_specs: Dict[str, str] = Field(...)
    search_queries: list[str] = Field(..., min_length=3, max_length=5)
    commercial_block: str = Field(...)
    missing_fields: list[str] = Field(default_factory=list)