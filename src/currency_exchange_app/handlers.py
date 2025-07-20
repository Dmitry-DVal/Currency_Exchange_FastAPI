# src/currency_exchange_app/exceptions/handlers.py
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from src.currency_exchange_app.exceptions import AppBaseException


async def app_base_exception_handler(request: Request, exc: AppBaseException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=HTTP_400_BAD_REQUEST, content={"message": exc.errors()}
#     )
#
#
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     first_error = exc.errors()[0]
#     error_message = first_error.get("msg", "Validation error")
#
#     if "loc" in first_error:
#         field = "->".join(str(x) for x in first_error["loc"])
#         error_message = f"{field}: {error_message}"
#
#     # Упрощаем ответ, удаляя несериализуемые данные
#     return JSONResponse(
#         status_code=HTTP_400_BAD_REQUEST, content={"message": error_message}
#     )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    for error in exc.errors():
        # Формируем понятное сообщение для каждой ошибки
        if "loc" in error:
            field = "->".join(str(x) for x in error["loc"])
            msg = error.get("msg", "Validation error")
            error_messages.append(f"{field}: {msg}")
        else:
            error_messages.append(error.get("msg", "Validation error"))

    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "message": "Validation error",
            "details": error_messages,  # Все сообщения об ошибках
        },
    )
