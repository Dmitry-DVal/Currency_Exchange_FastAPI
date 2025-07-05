# src/currency_exchange_app/services/exchange_rate.py
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from src.currency_exchange_app.exceptions import ExchangeRateNotFoundException
from src.currency_exchange_app.repositories.exchange_rate import ExchangeRateRepository
from src.currency_exchange_app.schemas.exchange_rate import ExchangeRateDTO, \
    InExchangeRatePairDTO
from src.currency_exchange_app.utils.decorators import db_exception_handler

logger = logging.getLogger("currency_exchange_app")


class ExchangeRateService:
    def __init__(self, session: AsyncSession):
        self.repo = ExchangeRateRepository(session)

    @db_exception_handler
    async def get_exchange_rate_by_code(self,
                                        code_pair: InExchangeRatePairDTO) -> ExchangeRateDTO:
        exchange_rate = await self.repo.get_by_code(code_pair)

        if not exchange_rate:
            logger.debug("Обменный курс для пары %s отсутствует в БД", code_pair)
            raise ExchangeRateNotFoundException(
                f"Обменный курс '{code_pair}' отсутствует.")

        return exchange_rate

    @db_exception_handler
    async def get_exchange_rates(self) -> list[ExchangeRateDTO]:
        return await self.repo.get_all()

