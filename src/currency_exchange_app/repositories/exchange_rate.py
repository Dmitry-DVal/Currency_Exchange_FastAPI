# src/currency_exchange_app/repositories/exchange_rate.py
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.currency_exchange_app.models import ExchangeRatesORM
from src.currency_exchange_app.schemas.exchange_rate import ExchangeRateDTO, \
    InExchangeRatePairDTO

logger = logging.getLogger("currency_exchange_app")


class ExchangeRateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_code(self, code_pair: InExchangeRatePairDTO) -> ExchangeRateDTO | None:
        stmt = select(ExchangeRatesORM).where(
            ExchangeRatesORM.baseCurrency.has(code=code_pair.base_currency),
            ExchangeRatesORM.targetCurrency.has(code=code_pair.target_currency)
        ).options(
            joinedload(ExchangeRatesORM.baseCurrency),
            joinedload(ExchangeRatesORM.targetCurrency)
        )

        logger.debug("SQL запрос get_by_code: %s", stmt)

        result = await self.session.execute(stmt)
        ex_rate_orm = result.scalar_one_or_none()

        if ex_rate_orm:
            return ExchangeRateDTO.model_validate(ex_rate_orm)
        return None


    async def get_all(self) -> list[ExchangeRateDTO]:
        """Получить все обменные курсы из БД."""
        stmt = select(ExchangeRatesORM).options(
            joinedload(ExchangeRatesORM.baseCurrency),
            joinedload(ExchangeRatesORM.targetCurrency)
        )
        logger.debug("Построение запроса query: %s", stmt)

        result = await self.session.execute(stmt)

        ex_rates_orm = result.scalars().all()
        logger.debug("Получение списка скаляров currencies_orm: %s", ex_rates_orm)

        ex_rates_list = [ExchangeRateDTO.model_validate(c) for c in ex_rates_orm]
        return ex_rates_list
