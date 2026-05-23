import datetime
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()


# генерируем JWT токен
def generate_token(user_id: int):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
    }

    return jwt.encode(payload, key=os.environ['SECRET_KEY'], algorithm=os.environ['ALGORITHM'])


# декодируем токен
def decode_token(token):
    return jwt.decode(token, key=os.environ['SECRET_KEY'], algorithms=[os.environ['ALGORITHM']])


# ключ для redis
def categories_key(user_id: int):
    return f'categories:{user_id}'


# ключ для users
def user_token_key(user_id: int):
    return f'user_token:{user_id}'
