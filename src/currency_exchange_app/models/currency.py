from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

# from ..db.base import Base
from src.currency_exchange_app.db.base import Base


class CurrenciesORM(Base):
    __tablename__ = 'Currencies'
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Code: Mapped[str] = mapped_column(VARCHAR(3), unique=True, nullable=False, )
    FullName: Mapped[str] = mapped_column(VARCHAR(50), unique=True, nullable=False)
    Sign: Mapped[str] = mapped_column(VARCHAR(3), unique=True, nullable=False)
