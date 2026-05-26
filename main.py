from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.transactions import router as transactions_router
from routers.categories import router as categories_router
from slowapi import _rate_limit_exceeded_handler
from limiter import limiter
from mongo_db import create_indexes

from slowapi.errors import RateLimitExceeded


async def lifespan(app: FastAPI):
    await create_indexes()  # логика, которая сработает при запуске приложения
    yield  # на этом моменте запускается приложение
    # по сути тут дальше идет логика что будет при выключении приложения


app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(auth_router)
app.include_router(transactions_router)
app.include_router(categories_router)
