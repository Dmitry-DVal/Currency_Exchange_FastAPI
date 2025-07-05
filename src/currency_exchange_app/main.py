# src/currency_exchange_app/main.py
from fastapi import FastAPI

from .api.currency import router as currency_router
from .api.exchange_rate import router as exchange_rate_router
from .logger import logger

logger.debug("🚀 Starting Currency Exchange app...")

app = FastAPI()

app.include_router(currency_router)
app.include_router(exchange_rate_router)


@app.get("/pings")
async def ping():
    return {"message": "pong"}
