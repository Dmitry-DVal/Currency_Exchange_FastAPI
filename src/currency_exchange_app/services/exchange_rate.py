# src/currency_exchange_app/services/exchange_rate.py
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_exchange_app.exceptions import (
    ExchangeRateNotFoundException,
    ExchangeRateAlreadyExistsException,
    CurrencyNotFoundException,
)
from src.currency_exchange_app.repositories import (
    CurrencyRepository,
    ExchangeRateRepository,
)
from src.currency_exchange_app.schemas.exchange_rate import (
    ExchangeRateDTO,
    InExchangeRatePairDTO,
    ExchangeRateCreateDTO,
    ExchangeRateUpdateDTO,
)
from src.currency_exchange_app.utils.decorators import db_exception_handler

logger = logging.getLogger("currency_exchange_app")


class ExchangeRateService:
    def __init__(self, session: AsyncSession):
        self.exchange_rate_repo = ExchangeRateRepository(session)
        self.currency_repo = CurrencyRepository(session)

    @db_exception_handler
    async def create_exchange_rate(
        self, exchange_rate_data: ExchangeRateCreateDTO
    ) -> ExchangeRateDTO:
        code_pair = InExchangeRatePairDTO(
            base_currency=exchange_rate_data.base_currency,
            target_currency=exchange_rate_data.target_currency,
        )
        base_currency_id, target_currency_id = await self._get_currency_ids(
            code_pair.base_currency, code_pair.target_currency
        )

        try:
            ex_rate_orm = await self.exchange_rate_repo.create(
                base_currency_id, target_currency_id, exchange_rate_data.rate
            )
            return ExchangeRateDTO.model_validate(ex_rate_orm)
        except IntegrityError as e:
            await self.exchange_rate_repo.session.rollback()
            if "foreign key constraint" in str(e).lower():
                raise CurrencyNotFoundException("Одна или обе валюты не найдены")
            logger.error("Exchange rate exists: %s", e)
            raise ExchangeRateAlreadyExistsException(
                f"Exchange Rate {exchange_rate_data.base_currency}/{exchange_rate_data.target_currency} Already Exists"
            )

    async def _get_currency_ids(
        self, base_currency: str, target_currency: str
    ) -> tuple[int, int]:
        base_currency_orm = await self.currency_repo.get_by_code(base_currency)
        target_currency_orm = await self.currency_repo.get_by_code(target_currency)

        if not base_currency_orm or not target_currency_orm:
            logger.debug(
                "Одна или обе валюты не найдены: %s", base_currency, target_currency
            )
            raise CurrencyNotFoundException(
                f"Одна или обе валюты с кодом {base_currency}/{target_currency} отсутствуют."
            )
        # return base_currency_orm.id, target_currency_orm.id
        return int(base_currency_orm.id), int(target_currency_orm.id)

    @db_exception_handler
    async def update_exchange_rate(
        self, new_rate: ExchangeRateUpdateDTO, code_pair: InExchangeRatePairDTO
    ) -> ExchangeRateDTO:
        new_ex_rate_orm = await self.exchange_rate_repo.update(
            new_rate.rate, **code_pair.model_dump()
        )
        if not new_ex_rate_orm:
            logger.debug("Обменный курс для пары %s отсутствует в БД", code_pair)
            raise ExchangeRateNotFoundException(
                f"Обменный курс '{code_pair}' отсутствует."
            )
        return ExchangeRateDTO.model_validate(new_ex_rate_orm)

    @db_exception_handler
    async def get_exchange_rate_by_currency_pair(
        self, code_pair: InExchangeRatePairDTO
    ) -> ExchangeRateDTO:
        ex_rate_orm = await self.exchange_rate_repo.get_by_currency_pair(
            **code_pair.model_dump()
        )

        if not ex_rate_orm:
            logger.debug("Обменный курс для пары %s отсутствует в БД", code_pair)
            raise ExchangeRateNotFoundException(
                f"Обменный курс '{code_pair}' отсутствует."
            )
        return ExchangeRateDTO.model_validate(ex_rate_orm)

    @db_exception_handler
    async def list_exchange_rates(self) -> list[ExchangeRateDTO]:
        ex_rates_orm_list = await self.exchange_rate_repo.get_all()
        logger.debug(
            "Получение списка скаляров currencies_orm длиной: %s",
            len(ex_rates_orm_list),
        )
        return [ExchangeRateDTO.model_validate(c) for c in ex_rates_orm_list]
