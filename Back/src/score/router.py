from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src import database
from src.auth import schemas, models

router = APIRouter()


@router.get("/top", response_model=dict)
async def get_top_players(db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        # Топ по количеству побед
        top_by_wins = await session.execute(
            select(models.User).order_by(models.User.wins.desc()).limit(20)
        )
        top_by_wins = top_by_wins.scalars().all()

        # Преобразуем top_by_wins в UserOut для сериализации
        top_by_wins_serialized = [
            schemas.UserOut(
                id=user.id,
                user_name=user.user_name,
                score=user.score,
                games_played=user.games_played,
                wins=user.wins,
                win_rate=(user.wins / user.games_played) if user.games_played > 0 else 0.0
            )
            for user in top_by_wins
        ]

        # Топ по соотношению побед/поражений (win_rate)
        # Учитываем только тех пользователей, у которых сыграно хотя бы 1 игра
        top_by_win_rate = await session.execute(
            select(models.User).where(models.User.games_played > 0)
            .order_by((models.User.wins / models.User.games_played).desc())
            .limit(20)
        )
        top_by_win_rate = top_by_win_rate.scalars().all()

        # Преобразуем top_by_win_rate в UserOut для сериализации
        top_by_win_rate_serialized = [
            schemas.UserOut(
                id=user.id,
                user_name=user.user_name,
                score=user.score,
                games_played=user.games_played,
                wins=user.wins,
                # win_rate рассчитываем вручную
                win_rate=(user.wins / user.games_played) if user.games_played > 0 else 0.0
            )
            for user in top_by_win_rate
        ]

        return {
            "top_by_wins": top_by_wins_serialized,  # Список пользователей с топом по победам
            "top_by_win_rate": top_by_win_rate_serialized,  # Список пользователей с топом по win_rate
        }


# Получение подробной информации о рейтинге пользователя
@router.get("/user/{user_id}/score", response_model=dict)
async def get_user_score(user_id: int, db: AsyncSession = Depends(database.get_db)):
    async with db as session:
        # Получение данных пользователя
        user_result = await session.execute(select(models.User).filter(models.User.id == user_id))
        user = user_result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Соотношение побед/поражений
        win_rate = user.wins / user.games_played if user.games_played > 0 else 0.0

        # Место в топе по количеству побед
        rank_by_wins_query = await session.execute(
            select(func.count()).where(models.User.wins > user.wins)
        )
        rank_by_wins = rank_by_wins_query.scalar() + 1  # Место пользователя по количеству побед

        # Место в топе по win_rate
        if user.games_played > 0:
            rank_by_win_rate_query = await session.execute(
                select(func.count()).where(
                    (models.User.wins / models.User.games_played)
                    > (user.wins / user.games_played)
                )
            )
            rank_by_win_rate = rank_by_win_rate_query.scalar() + 1  # Место пользователя по win_rate
        else:
            rank_by_win_rate = None  # Если пользователь не играл, ранк недоступен

        return {
            "status": "success",
            "data": {
                "user_name": user.user_name,
                "wins": user.wins,
                "win_rate": win_rate,
                "rank_by_wins": rank_by_wins,
                "rank_by_win_rate": rank_by_win_rate,
            },
            "details": None,
        }
