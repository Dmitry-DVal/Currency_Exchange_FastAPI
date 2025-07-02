import pytest
from httpx import AsyncClient, ASGITransport
from pytest_asyncio import fixture as async_fixture

from src.currency_exchange_app.main import app


@async_fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_get_currency_valid(async_client):
    response = await async_client.get("/currency/USD")
    assert response.status_code == 200
    assert response.json() == {
        "code": "USD",
        "name": "United States dollar",
        "id": 1,
        "sign": "$",
    }


@pytest.mark.asyncio
async def test_get_currency_not_found(async_client):
    response = await async_client.get("/currency/ZZZ")
    assert response.status_code == 404
    assert response.json() == {"detail": "Currency not found"}
    response = await async_client.get("/currency")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_currencies(async_client):
    response = await async_client.get("/currencies")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_post_currencies_sucsses(async_client):
    response = await async_client.post(
        "/currencies", json={"code": "RUB", "name": "Russian Rubl", "sign": "R"}
    )
    assert response.status_code == 201
    assert response.json() == {
        "code": "RUB",
        "name": "Russian Rubl",
        "sign": "R",
        "id": 3,
    }


@pytest.mark.asyncio
async def test_post_currency_conflict(async_client):
    # Код 'USD' уже есть
    response = await async_client.post(
        "/currencies", json={"name": "United States dollar", "code": "USD", "sign": "$"}
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Currency already exists"}


@pytest.mark.asyncio
async def test_post_currency_missing_field(async_client):
    response = await async_client.post(
        "/currencies",
        json={
            "code": "GBP",
            # нет name
            "sign": "£",
        },
    )
    assert response.status_code == 422
