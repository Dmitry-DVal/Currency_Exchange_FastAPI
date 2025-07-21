# src/currency_exchange_app/schemas/exchange_rate.py
from decimal import Decimal, InvalidOperation
from typing import Any

from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator
from pydantic_core import CoreSchema, core_schema

from .currency import CurrencyResponseDTO


class DecimalCommaDot(Decimal):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, v: str) -> Decimal:
        try:
            return Decimal(v.replace(",", "."))
        except InvalidOperation:
            raise ValueError("Некорректный формат числа")


class InExchangeRatePairDTO(BaseModel):  # 1
    """Базовая схема для валютной пары"""

    base_currency: str = Field(
        min_length=3,
        max_length=3,
        pattern=r"^[A-Za-z]+$",
        examples=["USD"],
    )
    target_currency: str = Field(
        min_length=3,
        max_length=3,
        pattern=r"^[A-Za-z]+$",
        examples=["RUB"],
    )

    @field_validator("base_currency", "target_currency")
    def uppercase_codes(cls, v):
        return v.upper()


class ExchangeRateCreateDTO(InExchangeRatePairDTO):  # 2
    """Создание обменного курса"""

    rate: DecimalCommaDot = Field(gt=0, examples=[Decimal("0.99")])

    @model_validator(mode="after")
    def check_different_currencies(self):
        if self.base_currency == self.target_currency:
            raise ValueError("Base and target currencies must be different.")
        return self


class ExchangeRateUpdateDTO(BaseModel):  # 3
    """Обновление курса"""

    rate: DecimalCommaDot = Field(gt=0, examples=[Decimal("0.99")])


class ExchangeRateDTO(BaseModel):  # 4
    """Ответ API для обменного курса"""

    id: int
    base_currency: CurrencyResponseDTO = Field(alias="baseCurrency")
    target_currency: CurrencyResponseDTO = Field(alias="targetCurrency")
    rate: Decimal = Field(examples=["81.00"])

    model_config = ConfigDict(from_attributes=True)
