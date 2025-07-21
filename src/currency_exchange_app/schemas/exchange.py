# src/currency_exchange_app/schemas/exchange.py
from decimal import Decimal, ROUND_HALF_UP

from pydantic import BaseModel, Field, ConfigDict, field_serializer

from .currency import CurrencyResponseDTO


class CurrencyConversionResultDTO(BaseModel):
    """Currency conversion result."""

    base_currency: CurrencyResponseDTO = Field(alias="baseCurrency")
    target_currency: CurrencyResponseDTO = Field(alias="targetCurrency")
    rate: Decimal = Field(description="Курс обмена base->target")
    amount: Decimal = Field(description="Исходная сумма")
    converted_amount: Decimal = Field(
        alias="convertedAmount", description="Конвертированная сумма"
    )

    @field_serializer("rate", "amount", "converted_amount")
    def serialize_decimal(self, v: Decimal) -> float:
        precision = Decimal("0.000001") if self.rate == v else Decimal("0.01")
        return float(v.quantize(precision, rounding=ROUND_HALF_UP))

    model_config = ConfigDict(from_attributes=True)
