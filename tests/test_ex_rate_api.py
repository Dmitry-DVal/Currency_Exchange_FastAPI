# tests/test_ex_rate_api.py

import pytest

from .control_cases import (
    RUB_CASE,
    USD_RESPONSE_CASE,
    RUB_RESPONSE_CASE,
    USD_RUB_RATE_CASE,
    USD_RUB_RATE_RESPONSE,
    EUR_USD_RATE_CASE,
    RATE_UPDATE_CASE,
    INVALID_NEGATIVE_RATE_RESPONSE,
    INVALID_RATE_CASE,
    INVALID_RATE_CASE_SAME_CURRENCY,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pair, status_code, response_data",
    [
        pytest.param("USDRUB", 200, USD_RUB_RATE_RESPONSE),
        pytest.param("usdRub", 200, USD_RUB_RATE_RESPONSE),
        pytest.param(
            "EURUSD",
            404,
            {
                "message": "The exchange rate of ‘base_currency='EUR' target_currency='USD'’ is not available."
            },
        ),
        pytest.param(
            "USDRUBEUR",
            400,
            {"message": "The currency pair code 'USDRUBEUR' is not correct."},
        ),
    ],
)
async def test_get_exchange_rate(
    async_client, _seed_db_with_rates, pair, status_code, response_data
):
    """Проверяем получение курса по паре валют"""
    response = await async_client.get(f"/exchangeRate/{pair}")
    assert response.status_code == status_code
    assert response.json() == response_data


@pytest.mark.asyncio
async def test_get_all_exchange_rates_empty(async_client, _clean_db):
    """Проверяем получение пустого списка курсов"""
    response = await async_client.get("/exchangeRates")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_all_exchange_rates(async_client, _seed_db_with_rates):
    """Проверяем получение списка всех курсов"""
    response = await async_client.get("/exchangeRates")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == USD_RUB_RATE_RESPONSE


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "rate_data, status_code, response_data",
    [
        pytest.param(USD_RUB_RATE_CASE, 201, USD_RUB_RATE_RESPONSE),
        pytest.param(
            EUR_USD_RATE_CASE,
            404,
            {"message": "One or both currencies with code EUR/USD are missing."},
        ),
        pytest.param(INVALID_RATE_CASE, 400, INVALID_NEGATIVE_RATE_RESPONSE),
        pytest.param(
            INVALID_RATE_CASE_SAME_CURRENCY,
            400,
            {
                "message": "body: Value error, Base and target currencies must be different."
            },
        ),
    ],
)
async def test_create_exchange_rate(
    async_client, _clean_db, _seed_db, rate_data, status_code, response_data
):
    """Проверяем создание нового курса"""
    await async_client.post("/currencies", data=RUB_CASE)
    response = await async_client.post("/exchangeRates", data=rate_data)
    assert response.status_code == status_code
    assert response.json() == response_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pair, update_data, status_code, response_data",
    [
        pytest.param(
            "USDRUB",
            RATE_UPDATE_CASE,
            200,
            {
                "id": 1,
                "baseCurrency": USD_RESPONSE_CASE,
                "targetCurrency": RUB_RESPONSE_CASE,
                "rate": "75.500000",
            },
        ),
        pytest.param(
            "EURUSD",
            RATE_UPDATE_CASE,
            404,
            {
                "message": "The exchange rate of ‘base_currency='EUR' target_currency='USD'’ is not available."
            },
        ),
        pytest.param(
            "USDRUB",
            INVALID_RATE_CASE,
            400,
            {"message": "body->rate: Input should be greater than 0"},
        ),
    ],
)
async def test_update_exchange_rate(
    async_client,
    _clean_db,
    _seed_db_with_rates,
    pair,
    update_data,
    status_code,
    response_data,
):
    """Проверяем обновление курса"""
    response = await async_client.patch(f"/exchangeRate/{pair}", data=update_data)
    assert response.status_code == status_code

    # Для Decimal нужно специальное сравнение
    if status_code == 200:
        result = response.json()
        assert result["id"] == response_data["id"]
        assert result["baseCurrency"] == response_data["baseCurrency"]
        assert result["targetCurrency"] == response_data["targetCurrency"]
        assert str(result["rate"]) == response_data["rate"]
    else:
        assert response.json() == response_data
