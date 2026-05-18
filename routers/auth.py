# энд поинты регистрации и логина
from fastapi import APIRouter
from schemas import UserCreate, UserResponse, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
# Depends - способ сказать "эта функция зависит от другой функции, вызови её сначала и передай результат"
from fastapi import Depends
from services.auth import register_user, login_user

router = APIRouter()


# регистрация нового пользователя
@router.post("/register", response_model=UserResponse, status_code=201)
# валидация данных происходит на этом этапе автоматически, поэтому не нужно ее валидировать руками
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    # не забывать что это асинхронная функция
    new_user = await register_user(user, session)

    return new_user


# авторизация пользователя
@router.post("/login")
async def login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    return await login_user(user, session)
