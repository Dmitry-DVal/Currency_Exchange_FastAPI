# src/currency_exchange_app/exceptions.py
from fastapi import status
from fastapi.responses import JSONResponse


class AppBaseException(Exception):
    """Basic application exception"""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

    def to_response(self):
        return JSONResponse(
            status_code=self.status_code, content={"message": self.message}
        )


class CurrencyBaseException(AppBaseException):
    """Basic currency exception"""


class CurrencyCodeError(CurrencyBaseException):
    """
    400: Currency code is not correct
    Example:
        {"message":"Код валюты -3245 не корректен."}
    """

    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message)


class CurrencyNotFoundException(CurrencyBaseException):
    """
    404: The currency doesn't exist.
    Example:
        {"message":"One or both currencies not found"}
    """

    def __init__(self, message: str = "Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)


class DatabaseException(AppBaseException):
    """
    500: Database or connection error.
    Example:
        {"message":"password authentication failed for user \"user_db"}
    """

    def __init__(self, message: str = "Database error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=message
        )


class CurrencyAlreadyExistsException(CurrencyBaseException):
    """
    409: The currency already exists
    Example:
        {"message": "Currency already exists"}
    """

    def __init__(self, message: str = "Currency already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, message=message)


class ExchangeRateBaseException(AppBaseException):
    """The basic exception for exchange rates."""


class ExchangeRatePairCodeError(ExchangeRateBaseException):
    """
    400: Currency code is not correct
    Example:
        {"message":"The currency pair code 'U3DIU7' is not correct."}
    """

    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message)


class ExchangeRateNotFoundException(ExchangeRateBaseException):
    """
    404: There is no exchange rate
    Example:
        {"message":"The exchange rate of ‘USDFRL’ is not available."}
    """

    def __init__(self, message: str = "Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)


class ExchangeRateAlreadyExistsException(ExchangeRateBaseException):
    """
    409: The exchange rate already exists
    Example:
        {"message": "Exchange Rate USDRUB Already Exists"}
    """

    def __init__(self, message: str = "Exchange Rate Already Exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, message=message)
