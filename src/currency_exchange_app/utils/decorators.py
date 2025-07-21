# src/currency_exchange_app/utils/decorators.py
import logging

from sqlalchemy.exc import SQLAlchemyError
from src.currency_exchange_app.exceptions import (
    DatabaseException,
    CurrencyAlreadyExistsException,
    CurrencyNotFoundException,
    ExchangeRateNotFoundException,
    ExchangeRateAlreadyExistsException,
)

logger = logging.getLogger("currency_exchange_app")


def db_exception_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (
            CurrencyAlreadyExistsException,
            CurrencyNotFoundException,
            ExchangeRateNotFoundException,
            ExchangeRateAlreadyExistsException,
        ) as error:
            raise error
        except SQLAlchemyError as e:
            logger.error("Ошибка SQLAlchemy: %s", e)
            raise DatabaseException("Database error")
        except Exception as e:
            logger.critical("Global error", exc_info=True)
            raise DatabaseException(str(e))

    return wrapper
