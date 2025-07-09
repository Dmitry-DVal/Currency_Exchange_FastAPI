# Тестовые данные
USD_CASE = {"code": "USD", "name": "United States dollar", "sign": "$"}

USD_RESPONSE_CASE = {
    "id": 1,
    "code": "USD",
    "name": "United States dollar",
    "sign": "$",
}

RUB_CASE = {"code": "RUB", "name": "Russian Ruble", "sign": "₽"}

RUB_NO_FIELD_CASE = {"code": "RUB", "name": "Russian Ruble"}

RUB_EXTRA_FIELD_CASE = {
    "code": "RUB",
    "name": "Russian Ruble",
    "sign": "₽",
    "nickname": "chervonet",
}

RUB_RESPONSE_CASE = {"id": 2, "code": "RUB", "name": "Russian Ruble", "sign": "₽"}

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

# Тестовые данные для обменных курсов
USD_RUB_RATE_CASE = {"base_currency": "USD", "target_currency": "RUB", "rate": 70.50}

EUR_USD_RATE_CASE = {"base_currency": "EUR", "target_currency": "USD", "rate": 1.10}

INVALID_RATE_CASE = {"base_currency": "USD", "target_currency": "RUB", "rate": -10.0}


RATE_UPDATE_CASE = {"rate": 75.50}

USD_RUB_RATE_RESPONSE = {
    "id": 1,
    "baseCurrency": USD_RESPONSE_CASE,
    "targetCurrency": RUB_RESPONSE_CASE,
    "rate": "70.500000",
}


INVALID_NEGATIVE_RATE_RESPONSE = {
    "detail": [
        {
            "type": "greater_than",
            "loc": ["body", "rate"],
            "msg": "Input should be greater than 0",
            "input": -10.0,
            "ctx": {"gt": 0},
        }
    ]
}
