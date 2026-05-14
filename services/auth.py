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
from repositories.user_repo import create_user, search_user

load_dotenv()

password_hash = PasswordHash([BcryptHasher()])


# хэширование пароля
async def register_user(user: UserCreate, session: AsyncSession):
    user_dict = user.model_dump()
    user_dict['password'] = password_hash.hash(user_dict['password'])
    # распаковка словаря, так как SQLAlchemy принимает только именнованные аргументы
    user_obj = User(**user_dict)
    await create_user(user=user_obj, session=session)
    return user_obj


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

    user_obj = await search_user(user_email, session=session)

    if not user_obj:
        raise HTTPException(status_code=401, detail='No such user')
    else:
        if not password_hash.verify(user_password, user_obj.password):
            raise HTTPException(status_code=401, detail='Wrong password')

    return {"access_token": generate_token(user_obj.id)}
