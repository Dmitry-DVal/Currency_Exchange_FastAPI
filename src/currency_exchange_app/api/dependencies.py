# src/currency_exchange_app/api/dependencies.py
from src.currency_exchange_app.services.exchange_rate import ExchangeRateService
from fastapi import Depends
from fastapi import Path
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_exchange_app.db import get_db
from src.currency_exchange_app.exceptions import (
    CurrencyCodeError,
    ExchangeRatePairCodeError,
)
from src.currency_exchange_app.schemas import CurrencyCodeDTO, InExchangeRatePairDTO
from src.currency_exchange_app.services import CurrencyService


def validate_currency_code(code: str = Path(...)) -> CurrencyCodeDTO:
    try:
        return CurrencyCodeDTO(code=code)
    except ValidationError:
        raise CurrencyCodeError(f"Код валюты {code} не корректен.")


def validate_currencies_pair_code(code_pair: str = Path(...)) -> InExchangeRatePairDTO:
    try:
        return InExchangeRatePairDTO(
            base_currency=code_pair[:3], target_currency=code_pair[3:]
        )
    except ValidationError:
        raise ExchangeRatePairCodeError(f"Код валютной пары {code_pair} не корректен.")


def get_currency_service(session: AsyncSession = Depends(get_db)) -> CurrencyService:
    return CurrencyService(session)


def get_ex_rate_service(session: AsyncSession = Depends(get_db)) -> ExchangeRateService:
    return ExchangeRateService(session)
