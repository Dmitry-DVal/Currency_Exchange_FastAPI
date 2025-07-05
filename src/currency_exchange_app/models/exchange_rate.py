from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.currency_exchange_app.db.base import Base


class ExchangeRatesORM(Base):
    __tablename__ = "ExchangeRates"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    baseCurrencyId: Mapped[int] = mapped_column(
        ForeignKey("Currencies.id"), nullable=False
    )
    targetCurrencyId: Mapped[int] = mapped_column(
        ForeignKey("Currencies.id"), nullable=False
    )
    rate: Mapped[float] = mapped_column(DECIMAL(9, 6), nullable=False)

    baseCurrency = relationship("CurrenciesORM", foreign_keys=[baseCurrencyId])
    targetCurrency = relationship("CurrenciesORM", foreign_keys=[targetCurrencyId])
