# src/currency_exchange_app/db/dependencies.py
from typing import AsyncGenerator

from .engine import async_session_factory


async def get_db() -> AsyncGenerator:
    """Session Generator for DI FastAPI."""
    async with async_session_factory() as session:
        yield session
