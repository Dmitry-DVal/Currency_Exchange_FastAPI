from fastapi import APIRouter, HTTPException

from сurrency_exchange_app.schemas.currency import CurrencyResponse, CurrencyCreate

router = APIRouter(tags=["Валюты"])

currencies = [
    CurrencyResponse(
        id=1,
        name="United States dollar",
        code="USD",
        sign="$"
    ),
    CurrencyResponse(
        id=2,
        name="Euro",
        code="EUR",
        sign="€"
    )
]


@router.get(
    "/currency/{code}",
    response_model=CurrencyResponse,
    summary="Получить валюту по коду",
    description="Возвращает полную информацию о валюте по её трёхбуквенному коду"
)
async def get_currency(
        code: str) -> CurrencyResponse:  # Должна возвращать модель валюты
    currency = next((c for c in currencies if c.code == code.upper()), None)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    return currency


@router.get("/currencies",
            summary="Получить все доступные валюты",
            description="Возвращает полную информацию о всех валютых"
            )
async def get_currencies() -> list[CurrencyResponse]:  # Возвращает список моделей
    return currencies


@router.post(
    "/currencies",
    response_model=CurrencyResponse,
    summary="Добавить валюту",
    description="Создаёт новую валюту в системе",
    response_description="Данные созданной валюты",
    responses={
        400: {"description": "Валюта с таким кодом уже существует"},
        201: {"description": "Валюта успешно создана"}
    }
)
async def create_currency(currency_data: CurrencyCreate) -> CurrencyResponse:
    if any(c.code == currency_data.code for c in currencies):
        raise HTTPException(status_code=400, detail="Currency already exists")

    new_currency = CurrencyResponse(
        id=len(currencies) + 1,
        **currency_data.model_dump()
    )
    currencies.append(new_currency)
    return new_currency
