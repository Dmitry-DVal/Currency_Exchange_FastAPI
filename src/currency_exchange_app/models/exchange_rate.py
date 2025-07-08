# src/currency_exchange_app/models/exchange_rate.py
from sqlalchemy import DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.currency_exchange_app.db.base import Base
from decimal import Decimal



class ExchangeRatesORM(Base):
    __tablename__ = "ExchangeRates"
    __table_args__ = (
        UniqueConstraint("baseCurrencyId", "targetCurrencyId",
                         name="uq_base_target_currency"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    baseCurrencyId: Mapped[int] = mapped_column(
        ForeignKey("Currencies.id"), nullable=False
    )
    targetCurrencyId: Mapped[int] = mapped_column(
        ForeignKey("Currencies.id"), nullable=False
    )
    rate: Mapped[Decimal] = mapped_column(DECIMAL(9, 6), nullable=False)

    baseCurrency = relationship("CurrenciesORM", foreign_keys=[baseCurrencyId])
    targetCurrency = relationship("CurrenciesORM", foreign_keys=[targetCurrencyId])


    def __repr__(self):
        return f"<{self.__class__.__name__}>"