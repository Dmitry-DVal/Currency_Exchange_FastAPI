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
        """Ищем валюту по коду. Возвращаем DTO или None (не найдено)."""
        stmt = select(CurrenciesORM).where(CurrenciesORM.code == code)
        logger.debug("SQL запрос get_by_code: %s", stmt)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[CurrenciesORM]:
        """Получить все валюты из БД."""
        stmt = select(CurrenciesORM)
        logger.debug("Построение запроса query: %s", stmt)

        result = await self.session.execute(stmt)
        logger.debug(
            "Запрос к БД, результат сырые данные row в формате Алхимии result: %s",
            result,
        )

        return result.scalars().all()

    async def create(self, code: str, name: str, sign: str) -> CurrenciesORM:
        """Добавить валюту в БД"""
        new_currency = CurrenciesORM(code=code, name=name, sign=sign)
        logger.debug("Создан ORM объект new_currency: %s", new_currency)

        self.session.add(new_currency)
        logger.debug("Регистрируем объект new_currency в текущей сессии SQLAlchemy")

        await self.session.commit()
        logger.debug("Выполнение INSERT в БД")

        await self.session.refresh(new_currency)
        return new_currency
