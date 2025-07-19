# src/currency_exchange_app/main.py
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.currency_exchange_app.exceptions import AppBaseException
from src.currency_exchange_app.handlers import (
    app_base_exception_handler,
    validation_exception_handler,
)
from .api.currency import router as currency_router
from .api.exchange import router as exchange_router
from .api.exchange_rate import router as exchange_rate_router
from .logger import logger
from .middlewares import register_middlewares

logger.debug("🚀 Starting Currency Exchange app...")

app = FastAPI()
register_middlewares(app)

app.add_exception_handler(AppBaseException, app_base_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]

app.include_router(currency_router)
app.include_router(exchange_rate_router)
app.include_router(exchange_router)
