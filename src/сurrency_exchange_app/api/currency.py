from fastapi import APIRouter

router = APIRouter(tags=["Валюты"])

currencies = [
    {
        "id": 1,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    {
        "id": 2,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    }
]


@router.get("/currency/{code}")
async def get_currency(code: str) -> dict: # Должна возвращать модель валюты
    return {
    "id": 0,
    "name": "Euro",
    "code": code,
    "sign": "€"
}

@router.get("/currencies")
async def get_currencies() -> list[dict]: # Возвращает список моделей
    return currencies

@router.post("/currencies")
async def post_currencies(name, code, sign) -> dict:
    currencies.append(
        {
            "id": len(currencies) + 1,
            "name": name,
            "code": code,
            "sign": sign
        }
    )
    return {"success": True}
