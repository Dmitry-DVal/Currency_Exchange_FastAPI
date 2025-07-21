# src/currency_exchange_app/db/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """The base class for all ORM models."""
    pass
