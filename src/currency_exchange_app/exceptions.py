# src/currency_exchange_app/exceptions.py
from fastapi import status
from fastapi.responses import JSONResponse


class AppBaseException(Exception):
    """Базовое исключение приложения"""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

    def to_response(self):
        return JSONResponse(
            status_code=self.status_code, content={"message": self.message}
        )


class CurrencyBaseException(AppBaseException):
    """Базовое исключение для валюты"""


class CurrencyCodeError(CurrencyBaseException):
    """
    400: Код валюты не корректен
    Пример:
        {"message":"Код валюты -3245 не корректен."}
    """

    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message)


class CurrencyNotFoundException(CurrencyBaseException):
    """
    404: Валюта не существует
    Пример:
        {"message":"Код валюты USr отсутствует."}
    """

    def __init__(self, message: str = "Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)


class DatabaseException(AppBaseException):
    """
    500: Ошибка базы данных или соединения.
    Пример:
        {"message":"password authentication failed for user \"user_db"}
    """

    def __init__(self, message: str = "Database error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=message
        )


class CurrencyAlreadyExistsException(CurrencyBaseException):
    """
    409: Валюта уже существует
    Пример:
        {"message": "Currency USD already exists"}
    """

    def __init__(self, message: str = "Currency already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, message=message)


class ExchangeRateBaseException(AppBaseException):
    """Базовое исключение для обменных курсов."""


class ExchangeRatePairCodeError(ExchangeRateBaseException):
    """
    400: Код валюты не корректен
    Пример:
        {"message":"Код валютной пары U3DIU7 не корректен."}
    """

    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message)


class ExchangeRateNotFoundException(ExchangeRateBaseException):
    """
    404: Обменный курс не существует
    Пример:
        {"message":"Обменный курс 'USDFRN' отсутствует."}
    """

    def __init__(self, message: str = "Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)


class ExchangeRateAlreadyExistsException(ExchangeRateBaseException):
    """
    409: Валютный курс уже существует
    Пример:
        {"message": "Exchange Rate USDRUB Already Exists"}
    """

    def __init__(self, message: str = "Exchange Rate Already Exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, message=message)
