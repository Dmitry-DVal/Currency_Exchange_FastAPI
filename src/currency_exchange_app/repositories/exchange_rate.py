# src/currency_exchange_app/repositories/exchange_rate.py
import logging

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_exchange_app.schemas.exchange_rate import ExchangeRateDTO
from src.currency_exchange_app.models import ExchangeRatesORM


logger = logging.getLogger("currency_exchange_app")


class ExchangeRateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all(self) -> list[ExchangeRateDTO]:
        """Получить все обменные курсы из БД."""
        # stmt = select(ExchangeRatesORM)
        stmt = select(ExchangeRatesORM).options(joinedload(ExchangeRatesORM.baseCurrency),
            joinedload(ExchangeRatesORM.targetCurrency)
        )
        logger.debug("Построение запроса query: %s", stmt)

        result = await self.session.execute(stmt)

        ex_rates_orm = result.scalars().all()
        logger.debug("Получение списка скаляров currencies_orm: %s", ex_rates_orm)

        ex_rates_list = [ExchangeRateDTO.model_validate(c) for c in ex_rates_orm]
        return ex_rates_list
