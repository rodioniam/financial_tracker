# синтаксис очень похож на SQLAlchemy модели, только наследование от другого класса
from pydantic import BaseModel
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


# то что отдаем клиенту
class UserResponse(UserBase):
    user_id: int
    created_at: datetime


# для работы внутри сервиса
class UserInDB(UserBase):
    user_id: int
    created_at: datetime
    hashed_pwd: str


# база для транзакции
class TransactionBase(BaseModel):
    date: datetime | None  # сервер сам подставит если пусто
    amount: Decimal
    type: TransactionType
    category_id: int


# создание транзакции
class TransactionCreate(TransactionBase):
    pass


# ответ клиенту и использование внутри сервиса
class TransactionResponse(TransactionBase):
    transaction_id: int
    user_id: int


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
