import repositories.analytics_repo as analytics_repo
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserInDB, CategoryAnalytics, MonthlyStats
from logger import log_event
from redis_client import get_redis_client
from .utils import category_amount_analytics_key, monthly_stats_key
import json


async def get_sum_by_categories(user: UserInDB, session: AsyncSession):
    cached = await get_redis_client().get(category_amount_analytics_key(user.id))

    if not cached:
        # model_dump(mode='json') автоматически приводит типы данных из модели в типы данных JSON
        query = [CategoryAnalytics.model_validate(dict(row._mapping)).model_dump(mode='json') for row in await analytics_repo.get_sum_by_categories(user.id, session)]
        await get_redis_client().set(category_amount_analytics_key(user.id), json.dumps(query), ex=3600)
        cached = json.dumps(query)

    await log_event('analytics_request', user.id, {'email': user.email})
    return json.loads(cached)


async def get_monthly_stats(user: UserInDB, session: AsyncSession):
    cached = await get_redis_client().get(monthly_stats_key(user.id))

    if not cached:
        query = [MonthlyStats.model_validate(dict(row._mapping)).model_dump(
            mode='json') for row in await analytics_repo.get_monthly_stats(user.id, session)]
        await get_redis_client().set(monthly_stats_key(user.id), json.dumps(query), ex=3600)
        cached = json.dumps(query)

    await log_event('monthly_stats_request', user.id, {'email': user.email})
    return json.loads(cached)
