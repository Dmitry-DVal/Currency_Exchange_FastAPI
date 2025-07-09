# src/currency_exchange_app/schemas/exchange.py
from decimal import Decimal, ROUND_HALF_UP

from pydantic import BaseModel, Field, ConfigDict, field_serializer

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

    @field_serializer("rate", "amount", "converted_amount")
    def serialize_decimal(self, v: Decimal) -> float:
        quantize_target = (
            Decimal("0.000001")
            if self.__class__.__name__ == "CurrencyConversionResultDTO"
            else Decimal("0.01")
        )
        return float(v.quantize(quantize_target, rounding=ROUND_HALF_UP))

    model_config = ConfigDict(from_attributes=True)
