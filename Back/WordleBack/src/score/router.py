from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src import database
from src.auth import schemas, models

router = APIRouter()


# Топ 10 пользователей по score
@router.get("/top", response_model=list[schemas.UserOut])
async def get_top_players(db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        result = await session.execute(select(models.User).order_by(models.User.score.desc()).limit(10))
        top_players = result.scalars().all()

        # Преобразуем топ игроков в формат, соответствующий UserOut
        return top_players  # Возвращаем только список пользователей


# Получение score конкретного пользователя
@router.get("/user/{user_name}/score", response_model=schemas.UserScore)
async def get_user_score(user_name: str, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        result = await session.execute(select(models.User).filter(models.User.user_name == user_name))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "status": "succsess",
            "data": [user],
            "details": None
        }
