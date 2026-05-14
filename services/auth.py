from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from schemas import UserCreate, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from repositories.user_repo import create_user, search_user_by_email, search_user_by_id
from .utils import generate_token, decode_token
from database import get_session


password_hash = PasswordHash([BcryptHasher()])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# хэширование пароля
async def register_user(user: UserCreate, session: AsyncSession):
    user_dict = user.model_dump()
    user_dict['password'] = password_hash.hash(user_dict['password'])
    # распаковка словаря, так как SQLAlchemy принимает только именнованные аргументы
    user_obj = User(**user_dict)
    await create_user(user=user_obj, session=session)
    return user_obj


# login пользователя
async def login_user(user: UserLogin, session: AsyncSession):
    user_dict = user.model_dump()
    user_email, user_password = user_dict['email'], user_dict['password']

    user_obj = await search_user_by_email(user_email, session=session)

    if not user_obj:
        raise HTTPException(status_code=401, detail='No such user')
    else:
        if not password_hash.verify(user_password, user_obj.password):
            raise HTTPException(status_code=401, detail='Wrong password')

    return {"access_token": generate_token(user_obj.id)}


# получение текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    user_id = decode_token(token)['user_id']
    user_obj = await search_user_by_id(user_id, session=session)

    if not user_obj:
        raise HTTPException(status_code=401, detail='Unauthorized')
    else:
        return user_obj
