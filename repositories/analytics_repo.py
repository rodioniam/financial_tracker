from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, extract
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
            func.sum(Transaction.amount).label('sum'),
            extract("YEAR", Transaction.date).label('year'),
            extract("MONTH", Transaction.date).label('month')
        ).where(
            Transaction.user_id == user_id
        ).group_by(
            Transaction.type,
            extract("YEAR", Transaction.date),
            extract("MONTH", Transaction.date)
        )
    )

    return query.all()
