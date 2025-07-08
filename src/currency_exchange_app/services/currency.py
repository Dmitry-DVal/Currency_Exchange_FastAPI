# src/currency_exchange_app/services/currency.py
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_exchange_app.exceptions import (
    CurrencyNotFoundException,
    CurrencyAlreadyExistsException,
)
from src.currency_exchange_app.repositories import CurrencyRepository
from src.currency_exchange_app.schemas import (
    CurrencyResponseDTO,
    CurrencyCreateDTO,
    CurrencyCodeDTO,
)
from src.currency_exchange_app.utils.decorators import db_exception_handler

logger = logging.getLogger("currency_exchange_app")


class CurrencyService:
    def __init__(self, session: AsyncSession):
        self.repo = CurrencyRepository(session)

    @db_exception_handler
    async def get_currency_by_code(
        self, code_dto: CurrencyCodeDTO
    ) -> CurrencyResponseDTO:
        currency_orm = await self.repo.get_by_code(code_dto.code)

        if not currency_orm:
            logger.debug("Валюты %s отсутствует в БД", code_dto)
            raise CurrencyNotFoundException(f"Валюта с кодом '{code_dto}' отсутствует.")

        return CurrencyResponseDTO.model_validate(currency_orm)

    @db_exception_handler
    async def get_currencies(self) -> list[CurrencyResponseDTO]:
        currencies_list_orm = await self.repo.get_all()
        logger.debug(
            "Получен список ORM моделей валют длиной %s", len(currencies_list_orm)
        )
        return [CurrencyResponseDTO.model_validate(c) for c in currencies_list_orm]

    @db_exception_handler
    async def create_currency(
        self, currency_data: CurrencyCreateDTO
    ) -> CurrencyResponseDTO:
        try:
            new_currency_orm = await self.repo.create(**currency_data.model_dump())
            return CurrencyResponseDTO.model_validate(new_currency_orm)
        except IntegrityError as e:
            await self.repo.session.rollback()
            logger.error("Currency exists: %s", e)
            raise CurrencyAlreadyExistsException("Currency already exists")
