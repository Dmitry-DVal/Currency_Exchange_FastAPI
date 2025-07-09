# src/currency_exchange_app/api/exchange.py
import logging
from decimal import Decimal

from fastapi import APIRouter, Depends, Query

from src.currency_exchange_app.api.dependencies import (
    get_exchange_service,
    validate_to_currency,
    validate_from_currency,
)
from src.currency_exchange_app.schemas import CurrencyConversionResultDTO
from src.currency_exchange_app.services import ExchangeService

router = APIRouter(tags=["Обмен валют"])
logger = logging.getLogger("currency_exchange_app")


@router.get("/exchange", response_model=CurrencyConversionResultDTO)
async def convert_currency(
    from_currency: str = Depends(validate_from_currency),
    to_currency: str = Depends(validate_to_currency),
    amount: Decimal = Query(..., gt=0),
    service: ExchangeService = Depends(get_exchange_service),
):
    """
    Конвертирует сумму из одной валюты в другую.
    Поддерживает 3 сценария получения курса:
    1. Прямой курс (A->B)
    2. Обратный курс (B->A)
    3. Кросс-курс через USD (A->USD->B)
    """
    logger.info(
        "Запрос конвертации валют из '%s' в '%s' к-во '%s'",
        from_currency,
        to_currency,
        amount,
    )
    return await service.convert_currency(from_currency, to_currency, amount)
