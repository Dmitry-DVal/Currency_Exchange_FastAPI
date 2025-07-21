# tests/test_currency_api.py
import pytest

from .control_cases import (
    USD_CASE,
    USD_RESPONSE_CASE,
    RUB_CASE,
    RUB_NO_FIELD_CASE,
    RUB_EXTRA_FIELD_CASE,
    RUB_RESPONSE_CASE,
    RUN_ERROR_FIELD_RESPONSE_CASE,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "currency_code, status_code, response_data",
    [
        pytest.param(
            "USD",
            200,
            USD_RESPONSE_CASE,
        ),
        pytest.param("uSd", 200, USD_RESPONSE_CASE),
        pytest.param(
            "EUR", 404, {"message": "Валюта с кодом 'code='EUR'' отсутствует."}
        ),
        pytest.param("usdEur", 400, {"message": "The currency code usdEur is not correct."}),
    ],
)
async def test_get_currency_by_code(
    async_client, _seed_db, currency_code, status_code, response_data
):
    """Проверяем получение валюты по коду"""
    response = await async_client.get(f"/currency/{currency_code}")

    assert response.status_code == status_code
    assert response.json() == response_data


@pytest.mark.asyncio
async def test_get_currencies(async_client, _clean_db, _seed_db):
    """Проверяем получение списка валют"""
    response = await async_client.get("/currencies")

    assert response.status_code == 200
    assert response.json() == [USD_RESPONSE_CASE]


@pytest.mark.asyncio
async def test_get_currencies_empty(async_client, _clean_db):
    response = await async_client.get("/currencies")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_several_currencies(async_client, _clean_db, _seed_db):
    await async_client.post("/currencies", data=RUB_CASE)
    response = await async_client.get("/currencies")
    assert response.status_code == 200
    assert response.json() == [USD_RESPONSE_CASE, RUB_RESPONSE_CASE]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "currency_data, status_code, response_data",
    [
        pytest.param(RUB_CASE, 201, RUB_RESPONSE_CASE),
        pytest.param(RUB_EXTRA_FIELD_CASE, 201, RUB_RESPONSE_CASE),
        pytest.param(USD_CASE, 409, {"message": "Currency already exists"}),
        pytest.param(RUB_NO_FIELD_CASE, 400, RUN_ERROR_FIELD_RESPONSE_CASE),
    ],
)
async def test_post_currency(
    async_client, _seed_db, currency_data, status_code, response_data
):
    """Проверяем добавление валюты."""
    response = await async_client.post("/currencies", data=currency_data)

    assert response.status_code == status_code
    assert response.json() == response_data
