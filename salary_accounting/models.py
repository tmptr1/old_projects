from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, text, Numeric, Integer, func
import datetime
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]
# intgr = Annotated[int, mapped_column(Integer, nullable=True)]
numeric = Annotated[Numeric, mapped_column(Numeric(12, 2), nullable=True)]

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("datetime('now', 'localtime')"))

class Payments(Base):
    __tablename__ = 'payments'
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    amount: Mapped[numeric]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("datetime('now', 'localtime')"))

