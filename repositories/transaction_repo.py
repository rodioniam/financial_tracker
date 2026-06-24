from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from models import Transaction, Category


async def create_transaction(transaction: Transaction, session: AsyncSession):
    session.add(transaction)
    await session.commit()
    return transaction


async def get_transaction_by_id(transaction_id: int, session: AsyncSession):
    search = await session.execute(select(Transaction).where(Transaction.id == transaction_id))
    transaction = search.scalar_one_or_none()

    return transaction


async def delete_transaction(transaction_id: int, session: AsyncSession):
    await session.execute(delete(Transaction).where(Transaction.id == transaction_id))
    await session.commit()


async def update_transaction(transaction_id: int, session: AsyncSession, data: dict):
    await session.execute(update(Transaction).where(Transaction.id == transaction_id).values(data))
    await session.commit()


# последний параметр позволяет передавать еще и название категории если нужно
async def filter_transactions(session: AsyncSession, user_id: int, date=None, category_id=None, type=None, with_category: bool = False):
    conditions = []  # список условий

    # список будет пополняться объектами SQLAlchemy
    conditions.append(Transaction.user_id == user_id)

    # если условие передано в функцию, то оно добавляется в список
    if date:
        conditions.append(Transaction.date == date)
    if category_id:
        conditions.append(Transaction.category_id == category_id)
    if type:
        conditions.append(Transaction.type == type)

    if with_category:
        query = await session.execute(
            select(
                Transaction,
                Category.name
            ).join(
                Category,
                Transaction.category_id == Category.id
            ).filter(*conditions)
        )

        return query.all()

    # метод filter() преобразует разархивированный список SQLAlchemy объектов в where условия через and
    search = await session.execute(select(Transaction).filter(*conditions))
    query = search.scalars().all()

    return query
