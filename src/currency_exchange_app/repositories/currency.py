# src/currency_exchange_app/repositories/currency.py
import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.currency_exchange_app.exceptions import (
    DatabaseException,
    CurrencyAlreadyExistsException,
)
from src.currency_exchange_app.models import CurrenciesORM
from src.currency_exchange_app.schemas import CurrencyResponseDTO, CurrencyCreateDTO

logger = logging.getLogger("currency_exchange_app")


class CurrencyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def db_get_currency_by_code(self, code: str) -> CurrencyResponseDTO | None:
        """Ищем валюту по коду. Возвращаем DTO или None (не найдено)."""
        stmt = select(CurrenciesORM).where(CurrenciesORM.Code == code)
        logger.debug("SQL запрос get_currency_by_code: %s", stmt)

        result = await self.session.execute(stmt)
        currency_orm = result.scalar_one_or_none()
        logger.debug("Получение скаляра currency_orm или None: %s", currency_orm)

        if currency_orm:
            return self._orm_to_dto(currency_orm)
        return None

    def _orm_to_dto(self, orm_obj: CurrenciesORM) -> CurrencyResponseDTO:
        """Приватный метод преобразования"""
        return CurrencyResponseDTO(
            id=orm_obj.ID,
            code=orm_obj.Code,
            name=orm_obj.FullName,
            sign=orm_obj.Sign
        )

    async def get_currencies(self) -> list[CurrencyResponseDTO]:
        """Получить все валюты из БД."""
        stmt = select(CurrenciesORM)
        logger.debug("Построение запроса query: %s", stmt)

        try:
            result = await self.session.execute(stmt)
            logger.debug(
                "Запрос к БД, результат сырые данные row в формате Алхимии result: %s",
                result,
            )
        except (SQLAlchemyError, Exception) as e:
            logger.error("Database error: %s", e)
            raise DatabaseException(str(e))

        currencies_orm = result.scalars().all()
        logger.debug(f"Получение списка скаляров currencies_orm: {currencies_orm}")

        currency_list = [CurrencyResponseDTO.model_validate(c) for c in currencies_orm]
        logger.debug("Создаем DTO объекты из ORM моделей, currency_list length: %s",
                     len(currency_list))

        return currency_list

    async def create_currency(
            self, currency_data: CurrencyCreateDTO
    ) -> CurrencyResponseDTO:
        """Добавить валюту в БД"""
        new_currency = CurrenciesORM(
            Code=currency_data.code,
            FullName=currency_data.name,
            Sign=currency_data.sign,
        )
        logger.debug("Создан ORM объект new_currency: %s", new_currency)

        self.session.add(new_currency)
        logger.debug("Регистрируем объект new_currency в текущей сессии SQLAlchemy")

        try:
            await self.session.commit()
            logger.debug("Выполнение INSERT в БД")
            await self.session.refresh(new_currency)
        except IntegrityError as e:
            await self.session.rollback()
            logger.error("Currency exists: %s", e)
            raise CurrencyAlreadyExistsException("Currency already exists")
        except (SQLAlchemyError, Exception) as e:
            logger.error("Database error: %s", e)
            raise DatabaseException(str(e))

        return CurrencyResponseDTO.model_validate(new_currency)
