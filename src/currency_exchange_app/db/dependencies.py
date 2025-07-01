# src/currency_exchange_app/db/dependencies.py
from typing import AsyncGenerator

# from sqlalchemy.ext.asyncio import AsyncSession
from .engine import async_session_factory


async def get_db() -> AsyncGenerator:
    """Генератор сессий для DI FastAPI"""
    async with async_session_factory() as session:
        yield session
