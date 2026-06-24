from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request
from services.auth import get_current_user
from services.analytics import get_sum_by_categories, get_monthly_stats
from database import get_session
from schemas import CategoryAnalytics, MonthlyStats
from models import User
from limiter import limiter

router = APIRouter()


@router.get("/category/analytics", response_model=list[CategoryAnalytics], status_code=200, summary='get spending report, grouped by categories')
@limiter.limit("5/minute")
async def get_c_analytics(request: Request, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    query = await get_sum_by_categories(user, session)

    result = [q for q in query]

    return result


@router.get("/monthly", response_model=list[MonthlyStats], status_code=200, summary='get monthly spending report')
@limiter.limit("5/minute")
async def get_monthly(request: Request, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    query = await get_monthly_stats(user, session)
    result = [q for q in query]

    return result
