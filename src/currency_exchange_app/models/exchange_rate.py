from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from ..db.base import Base
from src.currency_exchange_app.db.base import Base

class ExchangeRatesORM(Base):
    __tablename__ = 'ExchangeRates'
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    BaseCurrencyId: Mapped[int] = mapped_column(
        ForeignKey('Currencies.ID'), nullable=False
    )
    TargetCurrencyId: Mapped[int] = mapped_column(
        ForeignKey('Currencies.ID'),
        nullable=False
    )
    Rate: Mapped[float] = mapped_column(DECIMAL(6), nullable=False)

    BaseCurrency = relationship("CurrenciesORM", foreign_keys=[BaseCurrencyId])
    TargetCurrency = relationship("CurrenciesORM", foreign_keys=[TargetCurrencyId])


