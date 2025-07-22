# src/currency_exchange_app/api/exchange.py
import logging

from fastapi import APIRouter, Depends, Query

from src.currency_exchange_app.api.dependencies import (
    get_exchange_service,
    validate_to_currency,
    validate_from_currency,
)
from src.currency_exchange_app.schemas import CurrencyConversionResultDTO, \
    DecimalCommaDot
from src.currency_exchange_app.services import ExchangeService

router = APIRouter(tags=["Обмен валют"])
logger = logging.getLogger("currency_exchange_app")


@router.get("/exchange", response_model=CurrencyConversionResultDTO)
async def convert_currency(
        from_currency: str = Depends(validate_from_currency),
        to_currency: str = Depends(validate_to_currency),
        amount: DecimalCommaDot = Query(..., gt=0, description="Must be positive"),
        service: ExchangeService = Depends(get_exchange_service),
):
    logger.info(
        "Currency conversion request from ‘%s’ to ‘%s’ amount '%s'",
        from_currency,
        to_currency,
        amount,
    )
    return await service.convert_currency(from_currency, to_currency, amount)
