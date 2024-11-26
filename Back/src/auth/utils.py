from typing import Optional

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.database import get_db
from src.auth.models import User
from src.game.OptionalOAuth2 import OptionalOAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Хеширование пароля
def get_password_hash(password):
    return pwd_context.hash(password)


# Проверка пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Секретный ключ для кодирования JWT
SECRET_KEY = "biba"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

optional_oauth2_scheme = OptionalOAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user_from_token(token: str, db: AsyncSession):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Получаем пользователя из базы данных
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
        token: Optional[str] = Depends(optional_oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    if token is None:
        return None  # Возвращаем None для анонимного пользователя

    # Проверяем токен, если он существует
    user = await get_user_from_token(token, db)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user