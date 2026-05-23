from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import pytest_asyncio
# Это HTTP клиент из библиотеки httpx который умеет работать с async кодом.
# Он делает запросы к FastAPI приложению в тестах - так же как Postman, только в коде.
from httpx import AsyncClient, ASGITransport
from dotenv import load_dotenv
import os
from database import Base, get_session
from main import app
import fakeredis


load_dotenv()

DATABASE_URL = f"postgresql+asyncpg://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@localhost:5432/{os.environ['TEST_DB_NAME']}"


# fixture для pytest с созданием пустых баз для моделей
@pytest_asyncio.fixture()
async def db_session():
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    # создает таблицы с моделями
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # отдает сессию кдиенту
    async with async_session() as session:
        yield session
    # очищает таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# создание тестовой сессии для отправки клиенту
@pytest_asyncio.fixture()
async def client(db_session):
    app.dependency_overrides[get_session] = lambda: db_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# тестовый пользователь
@pytest_asyncio.fixture()
async def auth_client(client):
    await client.post(url='/register', json={
        'email': 'test_test@mail.com',
        'name': 'John',
        'last_name': 'Doe',
        'password': '1234'
    })

    response = await client.post(url='/login', json={
        'email': 'test_test@mail.com',
        'password': '1234'
    })

    token = response.json()['access_token']
    client.headers['Authorization'] = f'Bearer {token}'

    yield client


@pytest_asyncio.fixture()
async def fake_redis_client():
    async with fakeredis.FakeAsyncRedis(decode_responses=True) as client:
        yield client
