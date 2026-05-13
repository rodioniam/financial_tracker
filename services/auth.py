from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from schemas import UserCreate, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from fastapi import HTTPException
import datetime
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

password_hash = PasswordHash([BcryptHasher()])


# хэширование пароля
async def register_user(user: UserCreate, session: AsyncSession):
    user_dict = user.model_dump()
    user_dict['password'] = password_hash.hash(user_dict['password'])
    # распаковка словаря, так как SQLAlchemy принимает только именнованные аргументы
    user = User(**user_dict)
    session.add(user)
    await session.commit()
    return user


# генерируем JWT токен
def generate_token(user_id: int):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
    }

    return jwt.encode(payload, key=os.environ['SECRET_KEY'], algorithm=os.environ['ALGORITHM'])


# login пользователя
async def login_user(user: UserLogin, session: AsyncSession):
    user_dict = user.model_dump()
    user_email, user_password = user_dict['email'], user_dict['password']
    # select(User) - SELECT запрос к таблице users. where - условие.
    search = await session.execute(select(User).where(User.email == user_email))
    user = search.scalar_one_or_none()  # вернёт объект User или None если не найден

    if not user:
        raise HTTPException(status_code=401, detail='No such user')
    else:
        if not password_hash.verify(user_password, user.password):
            raise HTTPException(status_code=401, detail='Wrong password')

    return {"access_token": generate_token(user.id)}
