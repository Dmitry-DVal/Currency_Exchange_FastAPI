# src/currency_exchange_app/services/exchange_rate.py
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_exchange_app.exceptions import ExchangeRateNotFoundException, \
    ExchangeRateAlreadyExistsException, CurrencyNotFoundException
from src.currency_exchange_app.repositories import CurrencyRepository
from src.currency_exchange_app.repositories.exchange_rate import ExchangeRateRepository
from src.currency_exchange_app.schemas.exchange_rate import ExchangeRateDTO, \
    InExchangeRatePairDTO, ExchangeRateCreateDTO, ExchangeRateUpdateDTO
from src.currency_exchange_app.utils.decorators import db_exception_handler

logger = logging.getLogger("currency_exchange_app")


class ExchangeRateService:
    def __init__(self, session: AsyncSession):
        self.exchange_rate_repo = ExchangeRateRepository(session)
        self.currency_repo = CurrencyRepository(session)

    @db_exception_handler
    async def update_exchange_rate(
            self,
            new_rate: ExchangeRateUpdateDTO,
            code_pair: InExchangeRatePairDTO
    ) -> ExchangeRateDTO:
        new_ex_rate = await self.exchange_rate_repo.update(code_pair, new_rate.rate)
        if not new_ex_rate:
            logger.debug("Обменный курс для пары %s отсутствует в БД", code_pair)
            raise ExchangeRateNotFoundException(
                f"Обменный курс '{code_pair}' отсутствует.")
        return new_ex_rate



    async def _get_currency_ids(
            self, code_pair: InExchangeRatePairDTO
    ) -> tuple[int, int]:
        base_currency = await self.currency_repo.get_by_code(code_pair.base_currency)
        target_currency = await self.currency_repo.get_by_code(
            code_pair.target_currency)

        if not base_currency or not target_currency:
            logger.debug("Одна или обе валюты не найдены: %s", code_pair)
            raise CurrencyNotFoundException(
                f"Одна или обе валюты с кодом {code_pair.base_currency}/{code_pair.target_currency} отсутствуют."
            )
        return base_currency.id, target_currency.id

    @db_exception_handler
    async def create_exchange_rate(
            self, exchange_rate_data: ExchangeRateCreateDTO
    ) -> ExchangeRateDTO:
        code_pair = InExchangeRatePairDTO(
            base_currency=exchange_rate_data.base_currency,
            target_currency=exchange_rate_data.target_currency,
        )
        base_currency_id, target_currency_id = await self._get_currency_ids(code_pair)

        try:
            return await self.exchange_rate_repo.create(base_currency_id,
                                                        target_currency_id,
                                                        exchange_rate_data.rate)
        except IntegrityError as e:
            await self.exchange_rate_repo.session.rollback()
            if "foreign key constraint" in str(e).lower():
                raise CurrencyNotFoundException("Одна или обе валюты не найдены")
            logger.error("Exchange rate exists: %s", e)
            raise ExchangeRateAlreadyExistsException(
                f"Exchange Rate {exchange_rate_data.base_currency}/{exchange_rate_data.target_currency} Already Exists")



    @db_exception_handler
    async def get_exchange_rate_by_currency_pair(self,
                                                 code_pair: InExchangeRatePairDTO) -> ExchangeRateDTO:
        exchange_rate = await self.exchange_rate_repo.get_by_currency_pair(code_pair)

        if not exchange_rate:
            logger.debug("Обменный курс для пары %s отсутствует в БД", code_pair)
            raise ExchangeRateNotFoundException(
                f"Обменный курс '{code_pair}' отсутствует.")
        return exchange_rate

    @db_exception_handler
    async def list_exchange_rates(self) -> list[ExchangeRateDTO]:
        return await self.exchange_rate_repo.get_all()
