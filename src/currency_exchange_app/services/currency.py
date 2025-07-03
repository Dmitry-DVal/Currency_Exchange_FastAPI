# src/currency_exchange_app/services/currency.py
import logging

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_exchange_app.exceptions import (
    CurrencyNotFoundException,
    DatabaseException,
    CurrencyCodeError,
    CurrencyAlreadyExistsException,
)
from src.currency_exchange_app.repositories import CurrencyRepository
from src.currency_exchange_app.schemas import CurrencyResponseDTO, CurrencyCreateDTO

logger = logging.getLogger("currency_exchange_app")


class CurrencyService:
    def __init__(self, session: AsyncSession):
        self.repo = CurrencyRepository(session)

    async def get_currency_by_code(self, code: str) -> CurrencyResponseDTO:
        try:
            currency = await self.repo.get_by_code(code)
        except ValidationError:
            logger.warning("Invalid currency code %s", code)
            raise CurrencyCodeError(f"Код валюты {code} не корректен.")
        except SQLAlchemyError as e:
            logger.error("Ошибка SQLAlchemy: %s", e)
            raise DatabaseException("Ошибка базы данных")
        except Exception as e:
            logger.critical("Глобальная ошибка", exc_info=True)
            raise DatabaseException(str(e))

        if not currency:
            logger.debug("Валюты %s отсутствует в БД", code)
            raise CurrencyNotFoundException(f"Код валюты {code} отсутствует.")

        return currency

    async def get_currencies(self) -> list[CurrencyResponseDTO]:
        try:
            currency_list = await self.repo.get_all()
        except SQLAlchemyError as e:
            logger.error("Ошибка SQLAlchemy: %s", e)
            raise DatabaseException("Ошибка базы данных")
        except Exception as e:
            logger.critical("Глобальная ошибка", exc_info=True)
            raise DatabaseException(str(e))

        return currency_list

    async def create_currency(
        self, currency_data: CurrencyCreateDTO
    ) -> CurrencyResponseDTO:
        try:
            new_currency = await self.repo.create(currency_data)
        except IntegrityError as e:
            await self.repo.session.rollback()
            logger.error("Currency exists: %s", e)
            raise CurrencyAlreadyExistsException("Currency already exists")
        except SQLAlchemyError as e:
            logger.error("Ошибка SQLAlchemy: %s", e)
            raise DatabaseException("Ошибка базы данных")
        except Exception as e:
            logger.critical("Глобальная ошибка", exc_info=True)
            raise DatabaseException(str(e))

        return new_currency
