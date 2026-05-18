# синтаксис очень похож на SQLAlchemy модели, только наследование от другого класса
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime
from decimal import Decimal
from models import TransactionType
from typing import Annotated


class UserBase(BaseModel):
    email: EmailStr
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
    date: datetime | None = None  # сервер сам подставит если пусто
    amount: Decimal
    description: str | None = None
    type: TransactionType
    category_id: int


# создание транзакции
class TransactionCreate(TransactionBase):
    pass


# ответ клиенту и использование внутри сервиса
class TransactionResponse(TransactionBase):
    id: int  # было transaction_id
    user_id: int


class TransactionUpdate(TransactionBase):
    date: datetime | None = None
    amount: Decimal | None = None
    description: str | None = None
    type: TransactionType | None = None
    category_id: int | None = None


# база категории
class CategoryBase(BaseModel):
    name: Annotated[str, Field(min_length=1)]
    description: str | None = None


# создание категории
class CategoryCreate(CategoryBase):
    pass


# ответ клиенту и внутри сервиса
class CategoryResponse(CategoryBase):
    id: int  # было category_id
    user_id: int


class CategoryUpdate(CategoryBase):
    name: Annotated[str, Field(min_length=1)] | None = None


# возникла ошибка - в респонс схемах поля category_id/transaction_id не соответствовали названиям в моделях.
# при создании записей клиент выдавал ошибку, хотя запись успешно создавалась, просто для респонса не совпадали поля
# такое поведение не правильно, нужно прибегать к "транзакционности" - либо все прошло успешно, либо не прошло ничего.
# В SQLAlchemy это решается через транзакции с rollback при ошибке, в данном проекте это не реализовано
