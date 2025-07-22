# src/currency_exchange_app/api/dependencies.py
import logging

from fastapi import Depends
from fastapi import Path, Query
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_exchange_app.db import get_db
from src.currency_exchange_app.exceptions import (
    CurrencyCodeError,
    ExchangeRatePairCodeError,
)
from src.currency_exchange_app.schemas import (
    CurrencyCodeDTO,
    InExchangeRatePairDTO,
)
from src.currency_exchange_app.services import (
    CurrencyService,
    ExchangeRateService,
    ExchangeService,
)

logger = logging.getLogger("currency_exchange_app")


def validate_currency_code(code: str = Path(...)) -> CurrencyCodeDTO:
    try:
        return CurrencyCodeDTO(code=code)
    except ValidationError:
        raise CurrencyCodeError(f"The currency code {code} is not correct.")


def validate_from_currency(code: str = Query(..., alias="from")):
    try:
        return CurrencyCodeDTO(code=code).code
    except ValidationError:
        raise CurrencyCodeError(f"The currency code {code} is not correct.")


def validate_to_currency(code: str = Query(..., alias="to")):
    try:
        return CurrencyCodeDTO(code=code).code
    except ValidationError:
        raise CurrencyCodeError(f"The currency code {code} is not correct.")


def validate_currencies_pair_code(code_pair: str = Path(...)) -> InExchangeRatePairDTO:
    try:
        return InExchangeRatePairDTO(
            base_currency=code_pair[:3], target_currency=code_pair[3:]
        )
    except ValidationError:
        raise ExchangeRatePairCodeError(
            f"The currency pair code '{code_pair}' is not correct."
        )


def get_currency_service(session: AsyncSession = Depends(get_db)) -> CurrencyService:
    return CurrencyService(session)


def get_ex_rate_service(session: AsyncSession = Depends(get_db)) -> ExchangeRateService:
    return ExchangeRateService(session)


async def get_exchange_service(session: AsyncSession = Depends(get_db)):
    return ExchangeService(session)
