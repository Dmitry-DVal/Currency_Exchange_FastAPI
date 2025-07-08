# src/currency_exchange_app/repositories/exchange_rate.py
import logging
from decimal import Decimal

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

    async def create(self, base_currency_id: int, target_currency_id: int,
                     rate: Decimal) -> ExchangeRateDTO:
        new_ex_rate = ExchangeRatesORM(baseCurrencyId=base_currency_id,
                                       targetCurrencyId=target_currency_id,
                                       rate=rate)
        # Добавляем в базу
        self.session.add(new_ex_rate)
        await self.session.commit()
        await self.session.refresh(new_ex_rate)

        # Обновляем объект
        stmt = self.get_query_with_currencies().where(
            ExchangeRatesORM.id == new_ex_rate.id)

        result = await self.session.execute(stmt)
        full_obj = result.scalar_one_or_none()

        return ExchangeRateDTO.model_validate(full_obj)

    async def get_by_currency_pair(self,
                                   code_pair: InExchangeRatePairDTO) -> ExchangeRateDTO | None:
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

        return ExchangeRateDTO.model_validate(ex_rate_orm)

    async def get_all(self) -> list[ExchangeRateDTO]:
        """Получить все обменные курсы из БД."""
        stmt = self.get_query_with_currencies()
        logger.debug("Построение запроса query: %s", stmt)

        result = await self.session.execute(stmt)

        ex_rates_orm = result.scalars().all()
        logger.debug("Получение списка скаляров currencies_orm: %s", ex_rates_orm)

        ex_rates_list = [ExchangeRateDTO.model_validate(c) for c in ex_rates_orm]
        return ex_rates_list

    def get_query_with_currencies(self):
        return select(ExchangeRatesORM).options(
            joinedload(ExchangeRatesORM.baseCurrency),
            joinedload(ExchangeRatesORM.targetCurrency)
        )
