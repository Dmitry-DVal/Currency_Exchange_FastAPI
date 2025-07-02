# src/currency_exchange_app/db/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех ORM моделей"""

    pass

    # def __repr__(self):
    #     cols = []
    #     for col in self.__table__.columns.key():
    #         cols.append(f"{col}={getattr(self, col)}")
    #     # for col in self.__table__.columns:
    #     #     cols.append(f"{col.name}={getattr(self, col.name)}")
    #     return f"<{self.__class__.__name__} {', '.join(cols)}>"
