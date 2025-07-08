# src/currency_exchange_app/api/exchange_rate.py
import logging

from fastapi import APIRouter, Depends

from src.currency_exchange_app.api.dependencies import (
    validate_currencies_pair_code,
    get_ex_rate_service,
)
from src.currency_exchange_app.schemas.exchange_rate import (
    ExchangeRateDTO,
    ExchangeRateCreateDTO,
    ExchangeRateUpdateDTO,
    InExchangeRatePairDTO,
)
from src.currency_exchange_app.services import ExchangeRateService

router = APIRouter(tags=["Обменные курсы"])

logger = logging.getLogger("currency_exchange_app")


@router.patch("/exchangeRate/{code_pair}", response_model=ExchangeRateDTO)
async def update_exchange_rate(
    new_rate: ExchangeRateUpdateDTO,
    code_pair: InExchangeRatePairDTO = Depends(validate_currencies_pair_code),
    service: ExchangeRateService = Depends(get_ex_rate_service),
) -> ExchangeRateDTO:
    logger.debug("Запрос на изменение валютного курса пары %s", code_pair)
    return await service.update_exchange_rate(new_rate, code_pair)


@router.post("/exchangeRates", response_model=ExchangeRateDTO, status_code=201)
async def create_exchange_rates(
    exchange_rate_data: ExchangeRateCreateDTO,
    service: ExchangeRateService = Depends(get_ex_rate_service),
) -> ExchangeRateDTO:
    logger.debug(
        "Запрос на добавления обменного курса валютной пары %s",
        exchange_rate_data.base_currency,
        exchange_rate_data.target_currency,
    )
    return await service.create_exchange_rate(exchange_rate_data)


@router.get("/exchangeRate/{code_pair}", response_model=ExchangeRateDTO)
async def get_exchange_rate(
    code_pair: InExchangeRatePairDTO = Depends(validate_currencies_pair_code),
    service: ExchangeRateService = Depends(get_ex_rate_service),
) -> ExchangeRateDTO:
    logger.debug("Запрос обменного курса валютной пары %s", code_pair)
    return await service.get_exchange_rate_by_currency_pair(code_pair)


@router.get("/exchangeRates", response_model=list[ExchangeRateDTO])
async def get_all_exchange_rates(
    service: ExchangeRateService = Depends(get_ex_rate_service),
) -> list[ExchangeRateDTO]:
    logger.debug("Запрос списка всех обменных курсов")
    return await service.list_exchange_rates()
