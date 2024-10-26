from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import database
from src.auth import schemas, models, utils
from src.auth.utils import get_password_hash, verify_password
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


# Регистрация пользователя
@router.post("/register", response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        result = await session.execute(select(models.User).filter(models.User.user_name == user.user_name))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = get_password_hash(user.password)
        new_user = models.User(user_name=user.user_name, password_hashed=hashed_password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return {
            "status": "succsess",
            "data": [new_user],
            "details": None
        }


# Авторизация пользователя
@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        # Проверяем, существует ли пользователь
        result = await session.execute(select(models.User).filter(models.User.user_name == form_data.username))
        db_user = result.scalars().first()

        # Проверка имени пользователя и пароля
        if not db_user or not verify_password(form_data.password, db_user.password_hashed):
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        # Генерация токена при успешной проверке
        access_token = utils.create_access_token(data={"sub": str(db_user.id)})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
