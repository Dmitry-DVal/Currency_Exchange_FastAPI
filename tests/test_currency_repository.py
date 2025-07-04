# tests/test_currency_repository.py

import pytest
from sqlalchemy.exc import IntegrityError
from src.currency_exchange_app.models import CurrenciesORM
from src.currency_exchange_app.repositories import CurrencyRepository
from src.currency_exchange_app.schemas import CurrencyCreateDTO
from .control_cases import USD_CASE, RUB_CASE


@pytest.mark.asyncio
async def test_get_by_code_returns_currency(async_session, _clean_db):
    currency = CurrenciesORM(**USD_CASE)
    async_session.add(currency)
    await async_session.commit()

    repo = CurrencyRepository(async_session)

    result = await repo.get_by_code("USD")

    assert result is not None
    assert result.code == "USD"
    assert result.name == "United States dollar"
    assert result.sign == "$"


@pytest.mark.asyncio
async def test_get_all_returns_currencies(async_session):
    currency = CurrenciesORM(**RUB_CASE)
    async_session.add(currency)
    await async_session.commit()

    repo = CurrencyRepository(async_session)

    result = await repo.get_all()

    assert result is not None
    assert len(result) == 2
    assert {c.code for c in result} == {"USD", "RUB"}


@pytest.mark.asyncio
async def test_create_returns_currency(async_session, _clean_db):
    currency = CurrencyCreateDTO(**USD_CASE)
    repo = CurrencyRepository(async_session)

    result = await repo.create(currency)

    assert result is not None
    assert result.code == "USD"
    assert result.name == "United States dollar"
    assert result.sign == "$"


@pytest.mark.asyncio
async def test_get_by_code_returns_none_for_non_existent(async_session):
    repo = CurrencyRepository(async_session)
    result = await repo.get_by_code("NON_EXISTENT")
    assert result is None


@pytest.mark.asyncio
async def test_get_all_returns_empty_list_for_empty_db(async_session, _clean_db):
    repo = CurrencyRepository(async_session)
    result = await repo.get_all()
    assert result == []


@pytest.mark.asyncio
async def test_create_duplicate_raises_error(async_session, _clean_db, _seed_db):
    repo = CurrencyRepository(async_session)
    currency = CurrencyCreateDTO(**USD_CASE)

    with pytest.raises(IntegrityError):
        await repo.create(currency)


@pytest.mark.asyncio
async def test_created_currency_persists(async_session, _clean_db):
    repo = CurrencyRepository(async_session)
    dto = CurrencyCreateDTO(**RUB_CASE)
    created = await repo.create(dto)

    fetched = await repo.get_by_code("RUB")
    assert fetched == created  # по значению DTO (не по id)
