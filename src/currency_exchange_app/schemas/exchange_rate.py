# src/currency_exchange_app/schemas/exchange_rate.py
from decimal import Decimal

from .currency import CurrencyResponseDTO
from pydantic import BaseModel, Field, field_validator, ConfigDict


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

    rate: Decimal = Field(gt=0, examples=[Decimal("0.99")])


class ExchangeRateUpdateDTO(BaseModel):  # 3
    """Обновление курса"""

    rate: Decimal = Field(
        gt=0,
        examples=[Decimal("0.99")],
        description="Новое значение курса (должно быть больше 0)",
    )


class ExchangeRateDTO(BaseModel):  # 4
    """Ответ API для обменного курса"""

    id: int
    base_currency: CurrencyResponseDTO = Field(alias="baseCurrency")
    target_currency: CurrencyResponseDTO = Field(alias="targetCurrency")
    rate: Decimal = Field(examples=["81.00"])

    model_config = ConfigDict(from_attributes=True)
