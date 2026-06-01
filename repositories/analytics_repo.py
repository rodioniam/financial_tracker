from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, extract, Integer
from models import Transaction, Category


async def get_sum_by_categories(user_id: int, session: AsyncSession):
    query = await session.execute(
        select(
            Transaction.category_id,
            Transaction.type,
            func.sum(Transaction.amount).label('sum'),
            Category.name
        ).join(
            Category,
            Transaction.category_id == Category.id
        ).where(
            Transaction.user_id == user_id
        ).group_by(
            Transaction.category_id,
            Transaction.type,
            Category.name
        )
    )

    return query.all()


async def get_monthly_stats(user_id: int, session: AsyncSession):
    query = await session.execute(
        select(
            Transaction.type,
            func.sum(Transaction.amount).label('amount'),
            extract("YEAR", Transaction.date).cast(Integer).label('year'),
            extract("MONTH", Transaction.date).cast(Integer).label('month')
        ).where(
            Transaction.user_id == user_id
        ).group_by(
            Transaction.type,
            extract("YEAR", Transaction.date),
            extract("MONTH", Transaction.date)
        )
    )

    return query.all()
