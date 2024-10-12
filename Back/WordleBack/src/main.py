from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.router import router as auth_router

from src.score.router import router as users_router
from src.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Tabeles's been created")
    yield
    print("Turning off")
app = FastAPI(lifespan=lifespan)

# Подключаем маршруты авторизации
app.include_router(auth_router)

# Подключаем маршруты для работы с пользователями
app.include_router(users_router, prefix="/users", tags=["users"])
