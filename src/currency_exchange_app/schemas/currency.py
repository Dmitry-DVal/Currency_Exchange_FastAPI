# src/currency_exchange_app/schemas/currency.py
from pydantic import BaseModel, Field, field_validator, ConfigDict


class CurrencyCodeDTO(BaseModel):
    """Только код валюты для поиска"""
    code: str = Field(min_length=3, max_length=3, pattern=r"^[A-Za-z]+$",
                      examples=["USD"], alias="Code")

    @field_validator("code")
    def uppercase_code(cls, v):
        return v.upper()


class CurrencyCreateDTO(CurrencyCodeDTO):
    """Данные для создания валюты"""
    name: str = Field(min_length=3, max_length=50, examples=["United States dollar"],
                      description="Полное название валюты", alias="FullName")
    sign: str = Field(min_length=1, max_length=3, examples=["$"], alias="Sign")


class CurrencyResponseDTO(CurrencyCreateDTO):
    """Полные данные валюты (ответ API)"""
    id: int = Field(alias="ID")

    model_config = ConfigDict(from_attributes=True)
