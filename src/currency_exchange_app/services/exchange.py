# src/currency_exchange_app/services/exchange.py
import logging
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_exchange_app.exceptions import CurrencyNotFoundException
from src.currency_exchange_app.schemas import CurrencyResponseDTO
from src.currency_exchange_app.utils.decorators import db_exception_handler
from src.currency_exchange_app.repositories import (
    CurrencyRepository,
    ExchangeRateRepository,
)
from src.currency_exchange_app.schemas.exchange import CurrencyConversionResultDTO
from src.currency_exchange_app.exceptions import ExchangeRateNotFoundException

logger = logging.getLogger("currency_exchange_app")


class ExchangeService:
    def __init__(self, session: AsyncSession):
        self.exchange_rate_repo = ExchangeRateRepository(session)
        self.currency_repo = CurrencyRepository(session)

    async def convert_currency(
        self, from_currency: str, to_currency: str, amount: Decimal
    ) -> CurrencyConversionResultDTO:
        logger.debug("Получаем валюты")
        base_currency = await self.get_currency_by_code(from_currency)
        target_currency = await self.get_currency_by_code(to_currency)

        logger.debug("Пытаемся найти прямой курс")
        rate = await self._get_direct_rate(base_currency.code, target_currency.code)

        if not rate:
            logger.debug("Прямого курса нет. Пытаемся найти обратный курс")
            rate = await self._get_reverse_rate(from_currency, to_currency)

        if not rate:
            logger.debug("Обратного курса тоже нет. Пытаемся найти кросс-курс")
            rate = await self._get_cross_rate(from_currency, to_currency)

        if not rate:
            raise ExchangeRateNotFoundException(
                f"Не удалось найти курс для пары {from_currency}/{to_currency}"
            )

        converted_amount = (amount * rate).quantize(Decimal("0.01"))

        return CurrencyConversionResultDTO(
            baseCurrency=base_currency,
            targetCurrency=target_currency,
            rate=rate,
            amount=amount,
            convertedAmount=converted_amount,
        )

    async def _get_direct_rate(
        self, from_currency: str, to_currency: str
    ) -> Decimal | None:
        """Пытается получить прямой курс"""
        rate = await self.exchange_rate_repo.get_rate_by_pair(
            from_currency, to_currency
        )
        return rate if rate else None

    async def _get_reverse_rate(
        self, from_currency: str, to_currency: str
    ) -> Decimal | None:
        """Пытается получить обратный курс и инвертировать его"""
        rate = await self.exchange_rate_repo.get_rate_by_pair(
            to_currency, from_currency
        )
        return Decimal(1) / rate if rate else None

    async def _get_cross_rate(
        self, from_currency: str, to_currency: str
    ) -> Decimal | None:
        """Вычисляет кросс-курс через USD"""
        usd_to_from = await self.exchange_rate_repo.get_rate_by_pair(
            "USD", from_currency
        )
        usd_to_to = await self.exchange_rate_repo.get_rate_by_pair("USD", to_currency)

        if usd_to_from and usd_to_to:
            return usd_to_to / usd_to_from
        return None

    @db_exception_handler
    async def get_currency_by_code(self, code: str) -> CurrencyResponseDTO:
        currency_orm = await self.currency_repo.get_by_code(code)

        if not currency_orm:
            logger.debug("Валюты %s отсутствует в БД", code)
            raise CurrencyNotFoundException(f"Валюта с кодом '{code}' отсутствует.")

        return CurrencyResponseDTO.model_validate(currency_orm)
