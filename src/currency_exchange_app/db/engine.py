# src/currency_exchange_app/db/engine.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.currency_exchange_app.config import settings

async_engine = create_async_engine(url=settings.DATABASE_URL, echo=False)

async_session_factory = async_sessionmaker(async_engine)
