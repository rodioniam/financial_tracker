# энд поинты регистрации и логина
from fastapi import APIRouter, Request, Depends
from schemas import UserCreate, UserResponse, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
# Depends - способ сказать "эта функция зависит от другой функции, вызови её сначала и передай результат"
from services.auth import register_user, login_user, get_current_user, logout_user
from models import User
from limiter import limiter


router = APIRouter()


# регистрация нового пользователя
@router.post("/register", response_model=UserResponse, status_code=201, summary='register new user')
# добавление лимита на 5 запросов в минуту
@limiter.limit("5/minute")
# валидация данных происходит на этом этапе автоматически, поэтому не нужно ее валидировать руками
# обязательно добавить Request для правильной работы slowapi limit
async def register(request: Request, user: UserCreate, session: AsyncSession = Depends(get_session)):
    # не забывать что это асинхронная функция
    new_user = await register_user(user, session)

    return new_user


# авторизация пользователя
@router.post("/login", summary='authorize user')
@limiter.limit("5/minute")
async def login(request: Request, user: UserLogin, session: AsyncSession = Depends(get_session)):
    return await login_user(user, session)


# получение текущего пользователя
@router.get("/me", response_model=UserResponse, summary='returns current user data')
async def get_me(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return user


# logout с добавлением токена в blacklist
@router.post("/logout")
async def log_out_user(result=Depends(logout_user)):
    return result
