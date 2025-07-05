# tests/test_currency_service.py
import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.currency_exchange_app.exceptions import (
    CurrencyNotFoundException,
    CurrencyAlreadyExistsException
)
from src.currency_exchange_app.models import CurrenciesORM
from src.currency_exchange_app.schemas import CurrencyCreateDTO
from src.currency_exchange_app.services.currency import CurrencyService
from .control_cases import RUB_CASE, USD_CASE


@pytest.mark.asyncio
class TestCurrencyAPI:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, async_session: AsyncSession, _clean_db, _seed_db):
        self.service = CurrencyService(async_session)
        self.session = async_session

    async def test_get_currency_by_code_success(self):
        result = await self.service.get_currency_by_code("USD")
        assert result.code == "USD"
        assert result.name == "United States dollar"
        assert result.sign == "$"

    async def test_get_currency_by_code_not_found(self):
        with pytest.raises(CurrencyNotFoundException) as exc_info:
            await self.service.get_currency_by_code("EUR")

        assert "Валюта с кодом 'EUR' отсутствует" in str(exc_info.value)

    async def test_get_currencies(self):
        test_currency = CurrenciesORM(**RUB_CASE)
        self.session.add(test_currency)
        await self.session.commit()

        result = await self.service.get_currencies()

        assert len(result) == 2
        assert {c.code for c in result} == {"USD", "RUB"}

    async def test_create_currency_success(self):
        currency_data = CurrencyCreateDTO(**RUB_CASE)

        result = await self.service.create_currency(currency_data)

        assert result.code == "RUB"
        assert result.name == "Russian Ruble"
        assert result.sign == "₽"

        from_db = await self.session.get(CurrenciesORM, result.id)
        assert from_db is not None
        assert from_db.code == "RUB"

    async def test_create_currency_already_exists(self):
        currency_data = CurrencyCreateDTO(**USD_CASE)

        with pytest.raises(CurrencyAlreadyExistsException) as exc_info:
            await self.service.create_currency(currency_data)

        assert "Currency already exists" in str(exc_info.value)
