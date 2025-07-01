# src/currency_exchange_app/repositories/currency.py
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.currency_exchange_app.models import CurrenciesORM
from src.currency_exchange_app.schemas import CurrencyResponseDTO, CurrencyCreateDTO

logger = logging.getLogger("currency_exchange_app")

class CurrencyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_currency_by_code(self, code: str) -> CurrencyResponseDTO | None:
        """Получаем валюту из БД по коду"""
        stmt = select(CurrenciesORM).where(CurrenciesORM.Code == code.upper())
        logger.debug("Построение запроса query: %s", stmt)

        result = await self.session.execute(stmt)
        logger.debug("Raw result type: %s", type(result))

        currency_orm = result.scalar_one_or_none()
        logger.debug("Получение скаляра currency_orm: %s",currency_orm)

        if currency_orm:
            return CurrencyResponseDTO.model_validate(currency_orm)
        return None


    async def get_currencies(self) -> list[CurrencyResponseDTO] | None:
        """Полючить все валюты из БД."""
        stmt = select(CurrenciesORM) # построение самого запроса.
        logger.debug("Построение запроса query: %s", stmt)

        result = await self.session.execute(stmt) # <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x0000023CCF4B7C50>
        logger.debug("Запрос к БД, результат сырые данные row в формате Алхимии result: %s", result)

        currencies_orm = result.scalars().all() # Преобразует результат в "скаляры" (отдельные значения).
        logger.debug(f"Получение списка скаляров currencies_orm: {currencies_orm}")

        if currencies_orm:
            logger.debug("Создаем DTO объекты из ORM моделей")
            currency_list = []

            for currency_orm in currencies_orm:
                currency_list.append(CurrencyResponseDTO.model_validate(currency_orm))
            return currency_list
        return None

    async def create_currency(self, currency_data: CurrencyCreateDTO) -> CurrencyResponseDTO:
        """Добавить валюту в БД"""
        new_currency = CurrenciesORM(Code=currency_data.code,
                    FullName=currency_data.name,
                    Sign=currency_data.sign)
        logger.debug("Создан ORM объект new_currency: %s", new_currency)

        self.session.add(new_currency)
        logger.debug("Регистрируем объект new_currency в текущей сессии SQLAlchemy")
        try:
            await self.session.commit()
            logger.debug("Выполнение INSERT в БД")
            await self.session.refresh(new_currency)  # Обновляем объект добавляем ID
        except IntegrityError as e:
            await self.session.rollback()
            logger.error("Currency exists: %s", e)
            raise ValueError("Currency exists")

        return CurrencyResponseDTO.model_validate(new_currency)
