# синтаксис очень похож на SQLAlchemy модели, только наследование от другого класса
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal
from models import TransactionType


class UserBase(BaseModel):
    email: str
    name: str
    last_name: str


# то что принимаем при регистрации
# наследует все из UserBase
class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


# то что отдаем клиенту
class UserResponse(UserBase):
    id: int
    created_at: datetime

    # Pydantic должен знать что может читать атрибуты объекта (например, SQLAlchemy объекта модели) а не только словарь.
    model_config = ConfigDict(from_attributes=True)


# для работы внутри сервиса
class UserInDB(UserBase):
    id: int
    created_at: datetime
    hashed_pwd: str


# база для транзакции
class TransactionBase(BaseModel):
    date: datetime | None  # сервер сам подставит если пусто
    amount: Decimal
    description: str | None
    type: TransactionType
    category_id: int


# создание транзакции
class TransactionCreate(TransactionBase):
    pass


# ответ клиенту и использование внутри сервиса
class TransactionResponse(TransactionBase):
    transaction_id: int
    user_id: int


class TransactionUpdate(TransactionBase):
    date: datetime | None
    amount: Decimal | None
    description: str | None
    type: TransactionType | None
    category_id: int | None


# база категории
class CategoryBase(BaseModel):
    name: str
    description: str | None


# создание категории
class CategoryCreate(CategoryBase):
    pass


# ответ клиенту и внутри сервиса
class CategoryResponse(CategoryBase):
    category_id: int
