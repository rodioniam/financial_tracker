from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from models import Category


async def create_category(category: Category, session: AsyncSession):
    session.add(category)
    await session.commit()
    return category


async def get_all_categories(session: AsyncSession, user_id: int):
    search = await session.execute(select(Category).where(Category.user_id == user_id))
    categories = search.scalars().all()

    return categories


# для работы сервиса
async def get_category_by_id(category_id: int, session: AsyncSession):
    search = await session.execute(select(Category).where(Category.id == category_id))
    category = search.scalar_one_or_none()

    return category


# для поиска пользователем
async def search_by_name(category_name: str, user_id: int, session: AsyncSession):
    search = await session.execute(select(Category).where(Category.name.ilike(category_name), Category.user_id == user_id))
    category = search.scalar_one_or_none()

    return category


async def update_category(category_id: int, session: AsyncSession, data: dict):
    await session.execute(update(Category).where(Category.id == category_id).values(data))
    await session.commit()


async def delete_category(category_id: int, session: AsyncSession):
    await session.execute(delete(Category).where(Category.id == category_id))
    await session.commit()
