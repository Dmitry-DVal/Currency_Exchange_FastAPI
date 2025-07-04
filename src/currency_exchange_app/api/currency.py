# src/currency_exchange_app/api/currency.py
import logging

from fastapi import APIRouter, Depends
from src.currency_exchange_app.api.dependencies import (
    get_currency_service,
    validate_currency_code,
)
from src.currency_exchange_app.schemas import CurrencyResponseDTO, CurrencyCreateDTO
from src.currency_exchange_app.services.currency import CurrencyService

router = APIRouter(tags=["Валюты"])

logger = logging.getLogger("currency_exchange_app")


@router.get("/currency/{code}", response_model=CurrencyResponseDTO)
async def get_currency(
        code: str = Depends(validate_currency_code),
        service: CurrencyService = Depends(get_currency_service),
) -> CurrencyResponseDTO:
    logger.debug("Запрос валюты: %s", code)
    return await service.get_currency_by_code(code)


@router.get("/currencies", response_model=list[CurrencyResponseDTO])
async def get_currencies(
        service: CurrencyService = Depends(get_currency_service),
) -> list[CurrencyResponseDTO]:
    logger.debug("Запрос списка всех валют")
    return await service.get_currencies()


@router.post("/currencies", response_model=CurrencyResponseDTO, status_code=201)
async def create_currency(
        currency_data: CurrencyCreateDTO,
        service: CurrencyService = Depends(get_currency_service),
) -> CurrencyResponseDTO:
    logger.debug("Запрос добавления валюты: %s", currency_data)
    return await service.create_currency(currency_data)
