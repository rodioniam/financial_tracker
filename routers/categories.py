from fastapi import APIRouter, Depends
from schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from services.categories import create_category, update_category, delete_category, get_categories, get_category_by_id, get_category_by_name
from services.auth import get_current_user

router = APIRouter()


# создание категории
@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create(category: CategoryCreate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    new_category = await create_category(category, session, user)

    return new_category


# вывод списка категорий пользователя
@router.get("/categories", response_model=list[CategoryResponse], status_code=200)
async def get_list(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    query = await get_categories(user, session)
    result = [q for q in query]

    return result


# FastAPI читает роуты сверху вниз. Если /categories/{category_id} стоит выше,
# то запрос /categories/search/Еда попадёт в него и FastAPI попытается конвертировать "search" в int
# поиск по имени
@router.get("/categories/search/{category_name}", response_model=CategoryResponse, status_code=200)
async def get_by_name(category_name: str, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await get_category_by_name(category_name, session, user)


# поиск по id
@router.get("/categories/{category_id}", response_model=CategoryResponse, status_code=200)
async def get_by_id(category_id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await get_category_by_id(category_id, session, user)


# обновить категорию
@router.patch("/categories/{category}", response_model=CategoryResponse, status_code=200)
async def update(category: int, data: CategoryUpdate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    changes = await update_category(category, session, user, data)

    return changes


# удалить категорию
@router.delete("/categories/{category}", response_model=CategoryResponse, status_code=200)
async def delete_ct(category: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    ct_to_delete = await get_category_by_id(category, session, user)
    await delete_category(category, session, user)

    return ct_to_delete
