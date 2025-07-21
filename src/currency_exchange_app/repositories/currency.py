# src/currency_exchange_app/repositories/currency.py
import logging
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_exchange_app.models import CurrenciesORM

logger = logging.getLogger("currency_exchange_app")


class CurrencyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_code(self, code: str) -> CurrenciesORM | None:
        """Looking for currency by code. Return ORM or None (not found)."""
        stmt = select(CurrenciesORM).where(CurrenciesORM.code == code)
        logger.debug("SQL request get_by_code: %s", stmt)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[CurrenciesORM]:
        """Get all currencies from the database."""
        stmt = select(CurrenciesORM)
        logger.debug("Query construction: %s", stmt)

        result = await self.session.execute(stmt)
        logger.debug(
            "Query to the DB, the result is raw row data in Alchemy result format: %s",
            result,
        )

        return result.scalars().all()

    async def create(self, code: str, name: str, sign: str) -> CurrenciesORM:
        """Add currency to the database."""
        new_currency = CurrenciesORM(code=code, name=name, sign=sign)
        logger.debug("An ORM object new_currency has been created: %s", new_currency)

        self.session.add(new_currency)
        logger.debug("Register new_currency object in the current SQLAlchemy session")

        await self.session.commit()
        logger.debug("INSERT execution in the database")

        await self.session.refresh(new_currency)
        return new_currency
