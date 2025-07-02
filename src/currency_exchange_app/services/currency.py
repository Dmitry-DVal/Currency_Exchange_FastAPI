# src/currency_exchange_app/services/currency.py
import logging

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.currency_exchange_app.exceptions import CurrencyCodeError
from src.currency_exchange_app.exceptions import CurrencyNotFoundException, \
    DatabaseException
from src.currency_exchange_app.repositories import CurrencyRepository
from src.currency_exchange_app.schemas import CurrencyResponseDTO
from src.currency_exchange_app.schemas.currency import CurrencyCodeDTO

logger = logging.getLogger("currency_exchange_app")


class CurrencyService:
    def __init__(self, session: AsyncSession):
        self.repo = CurrencyRepository(session)

    async def get_currency_by_code(self, code: str) -> CurrencyResponseDTO:

        try:
            validated_code = self._validate_code(code)
            currency = await self.repo.db_get_currency_by_code(validated_code)
        except ValidationError as e:
            logger.warning("Invalid currency code %s", code)
            raise CurrencyCodeError(f"Код валюты {code} не корректен.")
        except SQLAlchemyError as e:
            logger.error("Ошибка SQLAlchemy: %s", e)
            raise DatabaseException("Ошибка базы данных при поиске валюты")
        except Exception as e:
            logger.critical("Глобальная ошибка", exc_info=True)
            raise DatabaseException(str(e))

        if not currency:
            logger.debug("Валюты %s отсутствует в БД", code)
            raise CurrencyNotFoundException(f"Код валюты {code} отсутствует.")

        return currency

    def _validate_code(self, code: str) -> str:
        """Приватный метод валидации"""
        validated_code = CurrencyCodeDTO(code=code).code
        return validated_code
