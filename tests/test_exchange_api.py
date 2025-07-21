from decimal import Decimal

import pytest

from .control_cases import (
    CONVERT_DIRECT_CASE,
    CONVERT_REVERSE_CASE,
)


@pytest.mark.asyncio
async def test_convert_direct(async_client, _clean_db, _seed_db_with_rates):
    response = await async_client.get("/exchange", params=CONVERT_DIRECT_CASE["params"])
    assert response.status_code == 200
    data = response.json()
    for key in ["baseCurrency", "targetCurrency", "rate", "amount", "convertedAmount"]:
        assert data[key] == CONVERT_DIRECT_CASE["expected"][key]


@pytest.mark.asyncio
async def test_convert_reverse(async_client, _seed_db_with_rates):
    response = await async_client.get(
        "/exchange", params=CONVERT_REVERSE_CASE["params"]
    )
    assert response.status_code == 200
    data = response.json()
    assert round(Decimal(data["convertedAmount"]), 2) == Decimal(
        CONVERT_REVERSE_CASE["expected_converted"]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, status, message",
    [
        ({"from": "USD", "to": "RUB", "amount": -10}, 400, None),
        (
            {"from": "USD", "to": "ABC", "amount": 10},
            404,
            "There is no currency with the code",
        ),
    ],
)
async def test_convert_errors(
    async_client, _seed_db_with_rates, params, status, message
):
    response = await async_client.get("/exchange", params=params)
    assert response.status_code == status
    if message:
        assert message in response.text
