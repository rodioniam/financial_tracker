# Base, engine и session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

# просто читает переменные из .env и помещяет их в os.environ
load_dotenv()

# в проде лучше использовать os.environ.get('DB_USER'), так как если по какой то причине не сработает, то даст None, который можно обработать
# на данный момент у меня просто упадет без явной ошибки
DATABASE_URL = f"postgresql+asyncpg://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@localhost:5432/{os.environ['DB_NAME']}"

engine = create_async_engine(DATABASE_URL)

# По умолчанию SQLAlchemy после commit помечает все объекты как "устаревшие".
# При следующем обращении к атрибуту - идёт новый запрос в базу чтобы обновить данные.
# В async-контексте это проблема: сессия может быть уже закрыта, а я обращаюсь к атрибуту и получаю ошибку. expire_on_commit=False отключает это поведение.
async_session = async_sessionmaker(engine, expire_on_commit=False)

# SQLAlchemy по умолчанию обращается к связанным объектам через модель — например user.transactions - синхронно.
# В async-контексте это снова проблема. AsyncAttrs добавляет возможность обращаться к таким атрибутам через await.


class Base(AsyncAttrs, DeclarativeBase):
    pass
