# src/currency_exchange_app/api/currency.py
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Form
from src.currency_exchange_app.api.dependencies import (
    get_currency_service,
    validate_currency_code,
)
from src.currency_exchange_app.schemas import (
    CurrencyResponseDTO,
    CurrencyCreateDTO,
    CurrencyCodeDTO,
)
from src.currency_exchange_app.services import CurrencyService

router = APIRouter(tags=["Валюты"])

logger = logging.getLogger("currency_exchange_app")


@router.get("/currency/{code}", response_model=CurrencyResponseDTO)
async def get_currency(
    code_dto: CurrencyCodeDTO = Depends(validate_currency_code),
    service: CurrencyService = Depends(get_currency_service),
) -> CurrencyResponseDTO:
    logger.debug("Currency Request: %s", code_dto.code)
    return await service.get_currency_by_code(code_dto)


@router.get("/currencies", response_model=list[CurrencyResponseDTO])
async def get_currencies(
    service: CurrencyService = Depends(get_currency_service),
) -> list[CurrencyResponseDTO]:
    logger.debug("Request a list of all currencies.")
    return await service.get_currencies()


@router.post("/currencies", response_model=CurrencyResponseDTO, status_code=201)
async def create_currency(
    currency_data: Annotated[CurrencyCreateDTO, Form()],
    service: CurrencyService = Depends(get_currency_service),
) -> CurrencyResponseDTO:
    logger.debug("Request to add currency: %s", currency_data)
    return await service.create_currency(currency_data)
