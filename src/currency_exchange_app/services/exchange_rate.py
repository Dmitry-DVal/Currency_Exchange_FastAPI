# src/currency_exchange_app/services/exchange_rate.py
import logging

from src.currency_exchange_app.schemas.exchange_rate import ExchangeRateDTO
from sqlalchemy.ext.asyncio import AsyncSession
from src.currency_exchange_app.repositories.exchange_rate import ExchangeRateRepository
from src.currency_exchange_app.utils.decorators import db_exception_handler

logger = logging.getLogger("currency_exchange_app")


class ExchangeRateService:
    def __init__(self, session: AsyncSession):
        self.repo = ExchangeRateRepository(session)

    @db_exception_handler
    async def get_exchange_rates(self) -> list[ExchangeRateDTO]:
        return await self.repo.get_all()