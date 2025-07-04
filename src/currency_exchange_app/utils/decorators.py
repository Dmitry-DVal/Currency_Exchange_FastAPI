# src/currency_exchange_app/utils/decorators.py
import logging

from sqlalchemy.exc import SQLAlchemyError
from src.currency_exchange_app.exceptions import (
    DatabaseException,
    CurrencyAlreadyExistsException,
    CurrencyNotFoundException,
)

logger = logging.getLogger("currency_exchange_app")


def db_exception_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (CurrencyAlreadyExistsException, CurrencyNotFoundException):
            raise
        except SQLAlchemyError as e:
            logger.error("Ошибка SQLAlchemy: %s", e)
            raise DatabaseException("Ошибка базы данных")
        except Exception as e:
            logger.critical("Глобальная ошибка", exc_info=True)
            raise DatabaseException(str(e))

    return wrapper
