import repositories.transaction_repo as transaction_repo
from schemas import TransactionCreate, TransactionResponse, UserInDB
from sqlalchemy.ext.asyncio import AsyncSession
from models import Transaction
from fastapi import HTTPException


async def create_transaction(transaction: TransactionCreate, session: AsyncSession, current_user: UserInDB):
    transaction_dict = transaction.model_dump()
    transaction_dict['user_id'] = current_user.id
    transaction_obj = Transaction(**transaction_dict)
    await transaction_repo.create_transaction(transaction=transaction_obj, session=session)
    return transaction_obj


async def delete_transaction(transaction: int, session: AsyncSession, current_user: UserInDB):
    current_user_id = current_user.id
    current_transaction = await transaction_repo.get_transaction_by_id(transaction, session=session)

    if current_transaction is not None and current_transaction.user_id == current_user_id:
        await transaction_repo.delete_transaction(transaction, session=session)
    else:
        raise HTTPException(status_code=404, detail='Not found')
