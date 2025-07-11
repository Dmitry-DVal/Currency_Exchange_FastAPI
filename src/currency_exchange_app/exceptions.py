# src/currency_exchange_app/exceptions.py
from fastapi import HTTPException, status


class AppBaseException(HTTPException):
    """Базовое исключение приложения"""


class CurrencyBaseException(AppBaseException):
    """Базовое исключение для валюты"""


class CurrencyCodeError(CurrencyBaseException):
    """
    400: Код валюты не корректен
    Пример:
        {"detail":"Код валюты -3245 не корректен."}
    """

    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class CurrencyNotFoundException(CurrencyBaseException):
    """
    404: Валюта не существует
    Пример:
        {"detail":"Код валюты USr отсутствует."}
    """

    def __init__(self, detail: str = "Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DatabaseException(AppBaseException):
    """
    500: Ошибка базы данных или соединения.
    Пример:
        {"detail":"password authentication failed for user \"user_db"}
    """

    def __init__(self, detail: str = "Database error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class CurrencyAlreadyExistsException(CurrencyBaseException):
    """
    409: Валюта уже существует
    Пример:
        {"detail": "Currency USD already exists"}
    """

    def __init__(self, detail: str = "Currency already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ExchangeRateBaseException(AppBaseException):
    """Базовое исключение для обменных курсов."""


class ExchangeRatePairCodeError(ExchangeRateBaseException):
    """
    400: Код валюты не корректен
    Пример:
        {"detail":"Код валютной пары U3DIU7 не корректен."}
    """

    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ExchangeRateNotFoundException(ExchangeRateBaseException):
    """
    404: Обменный курс не существует
    Пример:
        {"detail":"Обменный курс 'USDFRN' отсутствует."}
    """

    def __init__(self, detail: str = "Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ExchangeRateAlreadyExistsException(ExchangeRateBaseException):
    """
    409: Валютный курс уже существует
    Пример:
        {"detail": "Exchange Rate USDRUB Already Exists"}
    """

    def __init__(self, detail: str = "Exchange Rate Already Exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
