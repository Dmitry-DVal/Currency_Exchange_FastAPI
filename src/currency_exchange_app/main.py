from fastapi import FastAPI

from .api.currency import router as currency_router
from .logger import logger

logger.debug("🚀 Starting Currency Exchange app...")

app = FastAPI()

app.include_router(currency_router)


@app.get("/pings")
async def ping():
    return {"message": "pong"}
