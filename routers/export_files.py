from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request
from services.auth import get_current_user
from services.transactions import get_transactions
from services.analytics import get_sum_by_categories, get_monthly_stats
from services.export_files import export_transactions_csv, export_sum_by_category_csv, export_monthly_stats_csv
from database import get_session
from models import User
from limiter import limiter
from datetime import datetime

router = APIRouter()


@router.get("/export/transactions", status_code=200, summary='export all user transactions in csv file')
@limiter.limit("5/minute")
async def export_transactions(request: Request, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session), date: datetime = None, category_id: int = None, type: str = None):
    transactions_list = await get_transactions(user, session, date, category_id, type, with_category=True)  # noqa
    return await export_transactions_csv(transactions_list)


@router.get("/export/categories/sum", status_code=200, summary='export categories analytics report in csv file')
@limiter.limit("5/minute")
async def export_categories_sum(request: Request, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    result = await get_sum_by_categories(user, session)

    return await export_sum_by_category_csv(result)


@router.get("/export/monthly", status_code=200, summary='export monthly analytics report in csv')
@limiter.limit("5/minute")
async def export_monthly_stats(request: Request, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    result = await get_monthly_stats(user, session)

    return await export_monthly_stats_csv(result)
