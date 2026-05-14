from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User


async def create_user(user: User, session: AsyncSession):
    session.add(user)
    await session.commit()
    return user


async def search_user_by_email(email: str, session: AsyncSession):
    # select(User) - SELECT запрос к таблице users. where - условие.
    search = await session.execute(select(User).where(User.email == email))
    user = search.scalar_one_or_none()

    return user


async def search_user_by_id(id: int, session: AsyncSession):
    search = await session.execute(select(User).where(User.id == id))
    user = search.scalar_one_or_none()

    return user
