import repositories.transaction_repo as transaction_repo
from schemas import TransactionCreate, TransactionUpdate, UserInDB
from sqlalchemy.ext.asyncio import AsyncSession
from models import Transaction
from fastapi import HTTPException
from logger import log_event
from redis_client import get_redis_client
from .utils import category_amount_analytics_key, monthly_stats_key


async def create_transaction(transaction: TransactionCreate, session: AsyncSession, current_user: UserInDB):
    transaction_dict = transaction.model_dump()
    transaction_dict['user_id'] = current_user.id
    transaction_obj = Transaction(**transaction_dict)
    await transaction_repo.create_transaction(transaction=transaction_obj, session=session)
    await log_event('create_transaction', current_user.id, {'email': current_user.email})
    await get_redis_client().delete(category_amount_analytics_key(current_user.id), monthly_stats_key(current_user.id))
    return transaction_obj


async def delete_transaction(transaction: int, session: AsyncSession, current_user: UserInDB):
    current_user_id = current_user.id
    current_transaction = await transaction_repo.get_transaction_by_id(transaction, session=session)

    if current_transaction is None or current_transaction.user_id != current_user_id:
        await log_event('delete_transaction_failed', current_user.id, {'email': current_user.email, 'reason': 'user or transaction not found'})
        raise HTTPException(status_code=404, detail='Not found')

    await transaction_repo.delete_transaction(transaction, session=session)
    await log_event('delete_transaction', current_user.id, {'email': current_user.email})
    await get_redis_client().delete(category_amount_analytics_key(current_user.id), monthly_stats_key(current_user.id))


async def update_transaction(transaction: int, session: AsyncSession, current_user: UserInDB, data: TransactionUpdate):
    current_user_id = current_user.id
    current_transaction = await transaction_repo.get_transaction_by_id(transaction, session)
    # с такими настройками я получу только те данные, которые были переданы и не None
    data_to_upload = data.model_dump(exclude_none=True, exclude_unset=True)

    if current_transaction is None or current_transaction.user_id != current_user_id:
        await log_event('update_transaction_failed', current_user.id, {
            'email': current_user.email,
            'reason': 'user or transaction not found'
        }
        )
        raise HTTPException(status_code=404, detail='Not found')

    await transaction_repo.update_transaction(transaction, session, data_to_upload)
    if 'amount' in data_to_upload:
        data_to_upload['amount'] = float(data_to_upload['amount'])
    if 'type' in data_to_upload:
        data_to_upload['type'] = str(data_to_upload['type'])
    await log_event('update_transaction', current_user.id, {
        'email': current_user.email,
        'current_transaction': {
            'amount': float(current_transaction.amount),
            'type': str(current_transaction.type),
            'category_id': current_transaction.category_id
        },
        'data_to_upload': data_to_upload
    }
    )
    await get_redis_client().delete(category_amount_analytics_key(current_user.id), monthly_stats_key(current_user.id))
    return await transaction_repo.get_transaction_by_id(transaction, session)


# одна
async def get_transaction(transaction: int, session: AsyncSession, current_user: UserInDB):
    current_user_id = current_user.id
    current_transaction = await transaction_repo.get_transaction_by_id(transaction, session)

    if current_transaction is None or current_transaction.user_id != current_user_id:
        await log_event('get_one_transaction_failed', current_user.id, {'email': current_user.email, 'reason': 'user or transaction not found'})
        raise HTTPException(status_code=404, detail='Not found')

    await log_event('get_one_transaction', current_user.id, {'email': current_user.email})
    return current_transaction


# список
async def get_transactions(current_user: UserInDB, session: AsyncSession, date=None, category_id=None, type=None, with_category: bool = False):
    await log_event('get_all_transactions', current_user.id, {'email': current_user.email})
    return await transaction_repo.filter_transactions(session=session, user_id=current_user.id, date=date, category_id=category_id, type=type, with_category=with_category)
