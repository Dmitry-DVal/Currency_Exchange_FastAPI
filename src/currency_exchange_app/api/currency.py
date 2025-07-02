# src/currency_exchange_app/api/currency.py
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.currency_exchange_app.db import get_db
from src.currency_exchange_app.repositories import CurrencyRepository
from src.currency_exchange_app.schemas import CurrencyCreateDTO, CurrencyResponseDTO
from src.currency_exchange_app.services.currency import CurrencyService

router = APIRouter(tags=["Валюты"])

logger = logging.getLogger("currency_exchange_app")


@router.get("/currency/{code}", response_model=CurrencyResponseDTO)
async def get_currency(
        code: str, session: AsyncSession = Depends(get_db)
) -> CurrencyResponseDTO:
    logger.debug("Запрос валюты: %s", code)
    service = CurrencyService(session)
    return await service.get_currency_by_code(code)


@router.get("/currencies", response_model=list[CurrencyResponseDTO])
async def get_currencies(
        session: AsyncSession = Depends(get_db),
) -> list[CurrencyResponseDTO]:
    logger.debug("Запрос списка всех валют")

    repo = CurrencyRepository(session)

    return await repo.get_currencies()


@router.post("/currencies", response_model=CurrencyResponseDTO, status_code=201)
async def create_currency(
        currency_data: CurrencyCreateDTO, session: AsyncSession = Depends(get_db)
) -> CurrencyResponseDTO:
    logger.debug("Запрос добавления валюты: %s", currency_data)

    repo = CurrencyRepository(session)

    return await repo.create_currency(currency_data)
