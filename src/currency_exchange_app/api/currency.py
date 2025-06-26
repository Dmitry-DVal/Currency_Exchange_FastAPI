import logging

from fastapi import APIRouter, HTTPException

from src.currency_exchange_app.schemas import CurrencyResponse, CurrencyCreate

router = APIRouter(tags=["Валюты"])

logger = logging.getLogger("currency_exchange_app")


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
    logger.debug("Запрос получения валюты: %s", code)
    currency = next((c for c in currencies if c.code == code.upper()), None)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    return currency


@router.get("/currencies",
            summary="Получить все доступные валюты",
            description="Возвращает полную информацию о всех валютых"
            )
async def get_currencies() -> list[CurrencyResponse]:  # Возвращает список моделей
    logger.debug("Запрос всех валют")
    return currencies


@router.post(
    "/currencies",
    status_code=201,
    response_model=CurrencyResponse,
    summary="Добавить валюту",
    description="Создаёт новую валюту в системе",
    response_description="Данные созданной валюты",
    responses={
        409: {"description": "Валюты с таким кодом уже существует"},
        201: {"description": "Валюта успешно создана"}
    }
)
async def create_currency(currency_data: CurrencyCreate) -> CurrencyResponse:
    logger.debug("Запрос добовления валюты: %s", currency_data.code)
    if any(c.code == currency_data.code for c in currencies):
        raise HTTPException(status_code=409, detail="Currency already exists")

    new_currency = CurrencyResponse(
        id=len(currencies) + 1,
        **currency_data.model_dump()
    )
    currencies.append(new_currency)
    return new_currency
