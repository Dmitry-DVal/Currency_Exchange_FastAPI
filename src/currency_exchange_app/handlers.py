# src/currency_exchange_app/exceptions/handlers.py
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from src.currency_exchange_app.exceptions import AppBaseException


async def app_base_exception_handler(request: Request, exc: AppBaseException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    for error in exc.errors():
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
            "details": error_messages,
        },
    )
