from fastapi import APIRouter, Depends
from schemas import TransactionCreate, TransactionUpdate, TransactionResponse
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from services.transactions import create_transaction, delete_transaction, update_transaction, get_transactions, get_transaction
from services.auth import get_current_user
from datetime import datetime


router = APIRouter()


# создание транзакции
# объект пользователя будет создан на основе функции get_current_user, которая внутри себя проверяет токен
# использование response_model позволяет заменить строки, которые я закментил ниже - делает автоматически валидацию
@router.post("/transactions", response_model=TransactionResponse, status_code=201)
async def create(transaction: TransactionCreate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    new_transaction = await create_transaction(transaction, session, user)
    # return_info = TransactionResponse.model_validate(new_transaction) # заменяет эти строки
    # print(return_info.model_dump()) # так как теперь возвращается объект SQLAlchemy, то читать его лучше так

    return new_transaction


# получение транзакций по фильтрам
# Pydantic схемы нужны только для тела запроса, query параметры передаются прямо в URL
@router.get("/transactions", response_model=list[TransactionResponse], status_code=200)
async def get_list(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session), date: datetime = None, category_id: int = None, type: str = None):
    query = await get_transactions(user, session, date, category_id, type)
    result = [q for q in query]

    return result


# получить транзакцию по id
@router.get("/transaction/{transaction_id}", response_model=TransactionResponse, status_code=200)
async def get_one(transaction_id: int, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await get_transaction(transaction_id, session, user)


# обновить транзакцию
# FastAPI может автоматически подставлять параметры из URL, например, в данном случае возьмет id транзакции для передачи в функцию
@router.patch("/transactions/{transaction_id}", response_model=TransactionResponse, status_code=200)
async def update(transaction_id: int, transaction: TransactionUpdate, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    changes = await update_transaction(transaction=transaction_id, session=session, current_user=user, data=transaction)

    return changes


# удалить транзакцию
@router.delete("/transactions/{transaction_id}", response_model=TransactionResponse, status_code=200)
async def delete_tr(transaction_id: int, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    tr_to_delete = await get_transaction(transaction=transaction_id, session=session, current_user=user)
    await delete_transaction(transaction=transaction_id, session=session, current_user=user)

    return tr_to_delete
