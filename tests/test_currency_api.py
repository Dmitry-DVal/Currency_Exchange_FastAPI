# tests/test_currency_api.py
import pytest

# Тестовые данные
USD_CASE = {"code": "USD", "name": "United States dollar", "sign": "$"}
USD_RESPONSE_CASE = {
    "id": 1,
    "code": "USD",
    "name": "United States dollar",
    "sign": "$",
}
RUB_CASE = {"code": "RUB", "name": "Russian Ruble", "sign": "R"}
RUB_NO_FIELD_CASE = {"code": "RUB", "name": "Russian Ruble"}
RUB_EXTRA_FIELD_CASE = {
    "code": "RUB",
    "name": "Russian Ruble",
    "sign": "R",
    "nickname": "chervonet",
}
RUB_RESPONSE_CASE = {"id": 2, "code": "RUB", "name": "Russian Ruble", "sign": "R"}
RUN_ERROR_FIELD_RESPONSE_CASE = {
    "detail": [
        {
            "type": "missing",
            "loc": ["body", "sign"],
            "msg": "Field required",
            "input": {"code": "RUB", "name": "Russian Ruble"},
        }
    ]
}


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
        pytest.param("EUR", 404, {"detail": "Валюта с кодом 'EUR' отсутствует."}),
        pytest.param("usdEur", 400, {"detail": "Код валюты usdEur не корректен."}),
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
    await async_client.post("/currencies", json=RUB_CASE)
    response = await async_client.get("/currencies")
    assert response.status_code == 200
    assert response.json() == [USD_RESPONSE_CASE, RUB_RESPONSE_CASE]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "currency_data, status_code, response_data",
    [
        pytest.param(RUB_CASE, 201, RUB_RESPONSE_CASE),
        pytest.param(RUB_EXTRA_FIELD_CASE, 201, RUB_RESPONSE_CASE),
        pytest.param(USD_CASE, 409, {"detail": "Currency already exists"}),
        pytest.param(RUB_NO_FIELD_CASE, 422, RUN_ERROR_FIELD_RESPONSE_CASE),
    ],
)
async def test_post_currency(
    async_client, _seed_db, currency_data, status_code, response_data
):
    """Проверяем добавление валюты."""
    response = await async_client.post("/currencies", json=currency_data)

    assert response.status_code == status_code
    assert response.json() == response_data
