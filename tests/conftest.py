# tests/conftest.py
import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import select

from src.currency_exchange_app.db import get_db
from src.currency_exchange_app.db.base import Base
from src.currency_exchange_app.main import app
from src.currency_exchange_app.models import CurrenciesORM, ExchangeRatesORM
from decimal import Decimal

# DATABASE_URL
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Создаем движок SQLite в памяти
test_async_engine = create_async_engine(
    url=DATABASE_URL,
    echo=False,
    connect_args={
        "check_same_thread": False
    },  # разрешение на использования соединений из разных потоков
    poolclass=StaticPool,  # Если не прописать каждое соединение будет новая БД
)
# Тестовый сессия
test_async_session_factory = async_sessionmaker(test_async_engine)


# Переопределяем get_db, чтобы использовать тестовую сессию
async def override_get_db():
    """Генератор сессий для тестов"""
    async with test_async_session_factory() as session:
        yield session


# fixture, которая инициализирует БД перед тестами
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Удалили таблицу
        await conn.run_sync(Base.metadata.create_all)  # Создаем таблицы
    yield


# HTTP клиент с переопределенной БД
@pytest_asyncio.fixture
async def async_client():
    app.dependency_overrides[get_db] = override_get_db  # noqa
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def _seed_db():
    async for session in override_get_db():
        await session.execute(
            delete(CurrenciesORM)
        )  # Очистка таблицы перед каждым тестом, чтобы избежать конфликтов
        await session.commit()

        currency = CurrenciesORM(code="USD", name="United States dollar", sign="$")
        session.add(currency)
        await session.commit()
        break


@pytest_asyncio.fixture
async def _clean_db():
    async for session in override_get_db():
        await session.execute(delete(CurrenciesORM))
        await session.execute(delete(ExchangeRatesORM))
        await session.commit()
        break


# Дополнения для проверки сервисного слоя
@pytest_asyncio.fixture
async def async_session():
    """Фикстура для тестовой сессии"""
    async with test_async_session_factory() as session:
        yield session


# Заполнения для обменных курсов
@pytest_asyncio.fixture
async def _seed_db_with_rates(_seed_db):
    async for session in override_get_db():
        # Сначала создаем валюту RUB, если её нет
        rub = await session.execute(
            select(CurrenciesORM).where(CurrenciesORM.code == "RUB")
        )
        if not rub.scalar_one_or_none():
            session.add(CurrenciesORM(code="RUB", name="Russian Ruble", sign="₽"))
            await session.commit()

        # Проверяем, существует ли уже курс USD-RUB
        existing_rate = await session.execute(
            select(ExchangeRatesORM).where(
                ExchangeRatesORM.baseCurrency.has(code="USD"),
                ExchangeRatesORM.targetCurrency.has(code="RUB"),
            )
        )
        if not existing_rate.scalar_one_or_none():
            # Создаем курс только если его нет
            rate = ExchangeRatesORM(
                baseCurrencyId=1,  # USD
                targetCurrencyId=2,  # RUB
                rate=Decimal("70.50"),
            )
            session.add(rate)
            await session.commit()
        break
