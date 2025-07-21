# src/currency_exchange_app/schemas/currency.py
from pydantic import BaseModel, Field, field_validator, ConfigDict
import re


class CurrencyCodeDTO(BaseModel):
    """Just the currency code to look up."""

    code: str = Field(
        min_length=3,
        max_length=3,
        pattern=r"^[A-Za-z]+$",
        examples=["USD"],
    )

    @field_validator("code")
    def uppercase_code(cls, v):
        return v.upper()


class CurrencyCreateDTO(CurrencyCodeDTO):
    """Data to create the currency."""

    name: str = Field(
        min_length=3,
        max_length=50,
        examples=["United States dollar"],
        description="Полное название валюты",
        # pattern=r"^[A-Za-z]+$"
    )
    sign: str = Field(min_length=1, max_length=3, examples=["$"])  # , alias="Sign")

    @field_validator("sign")
    def normalize_sign(cls, v: str) -> str:
        return v.strip()

    @field_validator("name")
    def normalize_name(cls, v: str) -> str:
        v = v.strip()

        if not re.fullmatch(r"^[A-Za-z\s]+$", v):
            raise ValueError(
                "The name should contain only Latin letters and spaces"
            )
        v = v.title()
        v = " ".join(v.split())
        return v


class CurrencyResponseDTO(CurrencyCreateDTO):
    """Complete currency data (API response)."""

    id: int = Field(
        examples=["1"],
        description="Уникальный id Валюты",
    )

    model_config = ConfigDict(from_attributes=True)
