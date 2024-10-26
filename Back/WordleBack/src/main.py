from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends

from src.auth.router import router as auth_router
from src.auth.utils import oauth2_scheme

from src.score.router import router as users_router
from src.game.router import router as game_router
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


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


# Подключаем маршруты для работы с пользователями
app.include_router(users_router, prefix="/users", tags=["users"])

# Подключаем маршруты для игры
app.include_router(game_router, prefix="/game", tags=["game"])
