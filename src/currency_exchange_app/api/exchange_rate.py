# src/currency_exchange_app/api/exchange_rate.py
import logging

from src.currency_exchange_app.services.exchange_rate import ExchangeRateService
from fastapi import APIRouter, Depends
from src.currency_exchange_app.api.dependencies import validate_currencies_pair_code, get_ex_rate_service
from src.currency_exchange_app.schemas.exchange_rate import ExchangeRateDTO, \
    ExchangeRateCreateDTO, ExchangeRateUpdateDTO, InExchangeRatePairDTO

router = APIRouter(tags=["Обменные курсы"])

logger = logging.getLogger("currency_exchange_app")

@router.get("/exchangeRate/{code_pair}", response_model=ExchangeRateDTO)
async def get_exchange_rate(
        code_pair: InExchangeRatePairDTO = Depends(validate_currencies_pair_code),
    service: ExchangeRateService = Depends(get_ex_rate_service)
) -> ExchangeRateDTO:
    print(code_pair)
    logger.debug("Запрос обменного курса валютной пары %s", code_pair)
    return await service.get_exchange_rate_by_code(code_pair)



@router.get("/exchangeRates", response_model=list[ExchangeRateDTO])
async def get_all_exchange_rates(
        service: ExchangeRateService = Depends(get_ex_rate_service)
) -> list[ExchangeRateDTO]:
    logger.debug("Запрос списка всех обменных курсов")
    return await service.get_exchange_rates()





#
# @router.post("/exchangeRates", response_model=ExchangeRateDTO)
# async def create_exchange_rates(
#         exchange_rate_data: ExchangeRateCreateDTO
# ) -> ExchangeRateDTO:
#     logger.debug("Запрос на добавления обменного курса валютной пары %s",
#                  exchange_rate_data.base_currency, exchange_rate_data.target_currency)
#     pass
#
#
# @router.patch("/exchangeRate/{code_pair}", response_model=ExchangeRateDTO)
# async def update_exchange_rates(new_rate: ExchangeRateUpdateDTO,
#                                 code_pair: InExchangeRatePairDTO = Depends(
#                                     validate_currencies_pair_code)) -> ExchangeRateDTO:
#     logger.debug("Запрос на изменение валютного курса пары %s", code_pair)
#     pass
