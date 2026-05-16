from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.transactions import router as transactions_router
from routers.categories import router as categories_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(transactions_router)
app.include_router(categories_router)
