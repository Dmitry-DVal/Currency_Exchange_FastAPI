# src/currency_exchange_app/models/currency.py
from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.currency_exchange_app.db import Base


class CurrenciesORM(Base):
    __tablename__ = "Currencies"
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Code: Mapped[str] = mapped_column(
        VARCHAR(3),
        unique=True,
        nullable=False,
    )
    FullName: Mapped[str] = mapped_column(VARCHAR(50), unique=True, nullable=False)
    Sign: Mapped[str] = mapped_column(VARCHAR(3), unique=True, nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__name__}, {self.FullName}>"
