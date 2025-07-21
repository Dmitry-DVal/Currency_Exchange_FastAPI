# src/currency_exchange_app/repositories/exchange_rate.py
import logging
from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.currency_exchange_app.models import ExchangeRatesORM

logger = logging.getLogger("currency_exchange_app")


class ExchangeRateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, base_currency_id: int, target_currency_id: int, rate: Decimal
    ) -> ExchangeRatesORM:
        """Creates an exchange rate."""
        new_ex_rate = ExchangeRatesORM(
            baseCurrencyId=base_currency_id,
            targetCurrencyId=target_currency_id,
            rate=rate,
        )
        # Adding to the database
        self.session.add(new_ex_rate)
        await self.session.commit()
        await self.session.refresh(new_ex_rate)

        # Updating the object
        stmt = self.get_query_with_currencies().where(
            ExchangeRatesORM.id == new_ex_rate.id
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(
        self, new_rate: Decimal, base_currency: str, target_currency: str
    ) -> ExchangeRatesORM | None:
        """Update the exchange rate."""
        existing_rate = await self.get_by_currency_pair(base_currency, target_currency)
        logger.debug("old_ex_rate %s", existing_rate)
        if not existing_rate:
            logger.debug("No exchange rate")
            return None

        existing_rate.rate = new_rate
        await self.session.commit()
        await self.session.refresh(existing_rate)

        full_stmt = self.get_query_with_currencies().where(
            ExchangeRatesORM.id == existing_rate.id
        )
        full_result = await self.session.execute(full_stmt)
        return full_result.scalar_one()

    async def get_by_currency_pair(
        self, base_currency: str, target_currency: str
    ) -> ExchangeRatesORM | None:
        """Get the exchange rate for a currency pair."""
        stmt = self.get_query_with_currencies().where(
            ExchangeRatesORM.baseCurrency.has(code=base_currency),
            ExchangeRatesORM.targetCurrency.has(code=target_currency),
        )

        logger.debug("SQL request get_by_currency_pair: %s", stmt)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[ExchangeRatesORM]:
        """Get all exchange rates from the database."""
        stmt = self.get_query_with_currencies()
        logger.debug("Constructing a query: %s", stmt)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    def get_query_with_currencies(self):
        return select(ExchangeRatesORM).options(
            joinedload(ExchangeRatesORM.baseCurrency),
            joinedload(ExchangeRatesORM.targetCurrency),
        )

    # Обмен валют
    async def get_rate_by_pair(
        self, base_currency: str, target_currency: str
    ) -> Decimal | None:
        """Returns the exchange rate for a currency pair or None if not found."""
        stmt = select(ExchangeRatesORM.rate).where(
            ExchangeRatesORM.baseCurrency.has(code=base_currency),
            ExchangeRatesORM.targetCurrency.has(code=target_currency),
        )
        logger.debug("Constructing a query: %s", stmt)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
