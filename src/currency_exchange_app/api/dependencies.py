# src/currency_exchange_app/api/dependencies.py
from fastapi import Depends
from fastapi import Path
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_exchange_app.db import get_db
from src.currency_exchange_app.exceptions import CurrencyCodeError, \
    ExchangeRatePairCodeError
from src.currency_exchange_app.schemas.currency import CurrencyCodeDTO
from src.currency_exchange_app.schemas.exchange_rate import InExchangeRatePairDTO
from src.currency_exchange_app.services.currency import CurrencyService


def validate_currency_code(code: str = Path(...)) -> str:
    try:
        return CurrencyCodeDTO(code=code).code
    except ValidationError:
        raise CurrencyCodeError(f"Код валюты {code} не корректен.")


def validate_currencies_pair_code(code_pair: str = Path(...)) -> InExchangeRatePairDTO:
    try:
        return InExchangeRatePairDTO(base_currency=code_pair[:3],
                                     target_currency=code_pair[3:])
    except ValidationError:
        raise ExchangeRatePairCodeError(f"Код валютной пары {code_pair} не корректен.")


def get_currency_service(session: AsyncSession = Depends(get_db)) -> CurrencyService:
    return CurrencyService(session)
