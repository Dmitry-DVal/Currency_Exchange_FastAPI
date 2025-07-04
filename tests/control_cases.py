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
