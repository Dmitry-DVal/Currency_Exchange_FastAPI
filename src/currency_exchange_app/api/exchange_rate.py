import logging

from fastapi import APIRouter, Depends
from src.currency_exchange_app.api.dependencies import validate_currencies_pair_code
from src.currency_exchange_app.schemas.exchange_rate import ExchangeRateDTO, \
    ExchangeRateCreateDTO, ExchangeRateUpdateDTO, InExchangeRatePairDTO

router = APIRouter(tags=["Обменные курсы"])

logger = logging.getLogger("currency_exchange_app")


@router.get("/exchangeRates", response_model=list[ExchangeRateDTO])
async def get_all_exchange_rates() -> list[ExchangeRateDTO]:
    logger.debug("Запрос всех обменных курсов")
    pass


@router.get("/exchangeRate/{code_pair}", response_model=ExchangeRateDTO)
async def get_exchange_rate(
        code_pair: InExchangeRatePairDTO = Depends(validate_currencies_pair_code)
) -> ExchangeRateDTO:
    logger.debug("Запрос обменного курса валютной пары %s", code_pair)
    pass


@router.post("/exchangeRates", response_model=ExchangeRateDTO)
async def create_exchange_rates(
        exchange_rate_data: ExchangeRateCreateDTO
) -> ExchangeRateDTO:
    logger.debug("Запрос на добавления обменного курса валютной пары %s",
                 exchange_rate_data.base_currency, exchange_rate_data.target_currency)
    pass


@router.patch("/exchangeRate/{code_pair}", response_model=ExchangeRateDTO)
async def update_exchange_rates(new_rate: ExchangeRateUpdateDTO,
                                code_pair: InExchangeRatePairDTO = Depends(
                                    validate_currencies_pair_code)) -> ExchangeRateDTO:
    logger.debug("Запрос на изменение валютного курса пары %s", code_pair)
    pass
