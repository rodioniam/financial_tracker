import repositories.categories_repo as categories_repo
from schemas import CategoryCreate, CategoryUpdate, UserInDB
from sqlalchemy.ext.asyncio import AsyncSession
from models import Category
from fastapi import HTTPException


async def create_category(category: CategoryCreate, session: AsyncSession, current_user: UserInDB):
    category_dict = category.model_dump()
    category_dict['user_id'] = current_user.id
    category_obj = Category(**category_dict)
    await categories_repo.create_category(category=category_obj, session=session)
    return category_obj


async def delete_category(category: int, session: AsyncSession, current_user: UserInDB):
    current_user_id = current_user.id
    current_category = await categories_repo.get_category_by_id(category, session)

    if current_category is not None and current_category.user_id == current_user_id:
        await categories_repo.delete_category(category, session)
    else:
        raise HTTPException(status_code=404, detail='Not found')


async def update_category(category: int, session: AsyncSession, current_user: UserInDB, data: CategoryUpdate):
    current_user_id = current_user.id
    current_category = await categories_repo.get_category_by_id(category, session)
    data_to_upload = data.model_dump(exclude_none=True, exclude_unset=True)

    if current_category is not None and current_category.user_id == current_user_id:
        await categories_repo.update_category(category, session, data_to_upload)
    else:
        raise HTTPException(status_code=404, detail='Not found')


# поиск списком
async def get_categories(user: UserInDB, session: AsyncSession):
    return await categories_repo.get_all_categories(session, user)


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
