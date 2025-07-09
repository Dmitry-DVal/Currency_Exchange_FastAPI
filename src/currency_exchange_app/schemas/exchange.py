# src/currency_exchange_app/schemas/exchange.py
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

from .currency import CurrencyResponseDTO


class CurrencyConversionResultDTO(BaseModel):
    """Результат конвертации валют"""

    base_currency: CurrencyResponseDTO = Field(alias="baseCurrency")
    target_currency: CurrencyResponseDTO = Field(alias="targetCurrency")
    rate: Decimal = Field(description="Курс обмена base->target")
    amount: Decimal = Field(description="Исходная сумма")
    converted_amount: Decimal = Field(
        alias="convertedAmount", description="Конвертированная сумма"
    )

    model_config = ConfigDict(from_attributes=True)
