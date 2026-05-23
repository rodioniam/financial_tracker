import repositories.categories_repo as categories_repo
from schemas import CategoryCreate, CategoryUpdate, UserInDB, CategoryResponse
from sqlalchemy.ext.asyncio import AsyncSession
from models import Category
from fastapi import HTTPException
from redis_client import redis_client
import json
from .utils import categories_key


async def create_category(category: CategoryCreate, session: AsyncSession, current_user: UserInDB):
    category_dict = category.model_dump()
    category_dict['user_id'] = current_user.id
    category_obj = Category(**category_dict)
    await categories_repo.create_category(category=category_obj, session=session)
    await redis_client.delete(categories_key(current_user.id))
    return category_obj


async def delete_category(category: int, session: AsyncSession, current_user: UserInDB):
    current_user_id = current_user.id
    current_category = await categories_repo.get_category_by_id(category, session)

    if current_category is not None and current_category.user_id == current_user_id:
        await categories_repo.delete_category(category, session)
        await redis_client.delete(categories_key(current_user.id))
    else:
        raise HTTPException(status_code=404, detail='Not found')


async def update_category(category: int, session: AsyncSession, current_user: UserInDB, data: CategoryUpdate):
    current_user_id = current_user.id
    current_category = await categories_repo.get_category_by_id(category, session)
    data_to_upload = data.model_dump(exclude_none=True, exclude_unset=True)

    if current_category is not None and current_category.user_id == current_user_id:
        await categories_repo.update_category(category, session, data_to_upload)
        await redis_client.delete(categories_key(current_user.id))
        return await get_category_by_id(category, session, current_user)
    else:
        raise HTTPException(status_code=404, detail='Not found')


# # поиск списком
# async def get_categories(user: UserInDB, session: AsyncSession):
#     return await categories_repo.get_all_categories(session, user.id)


# поиск списком + кеширование
async def get_categories(user: UserInDB, session: AsyncSession):
    cached = await redis_client.get(categories_key(user.id))

    if not cached:
        categories = [CategoryResponse.model_validate(c, from_attributes=True).model_dump() for c in await categories_repo.get_all_categories(session, user.id)]
        await redis_client.set(categories_key(user.id), json.dumps(categories), ex=3600)
        cached = json.dumps(categories)

    return json.loads(cached)


# поиск по id
async def get_category_by_id(category: int, session: AsyncSession, current_user: UserInDB):
    current_user_id = current_user.id
    current_transaction = await categories_repo.get_category_by_id(category, session)

    if current_transaction is not None and current_transaction.user_id == current_user_id:
        return current_transaction
    else:
        raise HTTPException(status_code=404, detail='Not found')


# поиск по названию
async def get_category_by_name(category: str, session: AsyncSession, current_user: UserInDB):
    current_user_id = current_user.id
    current_category = await categories_repo.search_by_name(category, current_user_id, session)

    if current_category is not None:
        return current_category
    else:
        raise HTTPException(status_code=404, detail='Not found')
