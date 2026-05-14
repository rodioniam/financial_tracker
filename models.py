from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey
from sqlalchemy import Enum as SAEnum
import datetime
from decimal import Decimal
from enum import Enum


# это способ создать константы
class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str]
    # будет интерпретированно как SQL now() datetime функция
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())  # noqa


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    amount: Mapped[Decimal]
    # если использую константы, созданные через Enum, то нужно делать колонку с такими параметрами
    type: Mapped[TransactionType] = mapped_column(SAEnum(TransactionType))
    description: Mapped[str | None]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]  # способ сделать поле опциональным
