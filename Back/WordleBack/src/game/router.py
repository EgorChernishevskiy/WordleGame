from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src import database
from src.auth.utils import get_current_user
from src.game import models, schemas
from src.auth.models import User
from src.game.utils import generate_target_word

router = APIRouter()


@router.post("/game/start", response_model=schemas.GameStart)
async def start_game(
        db: AsyncSession = Depends(database.get_db), current_user: User = Depends(get_current_user)
):
    target_word = generate_target_word()
    new_game = models.Game(user_id=current_user.id, target_word=target_word)
    db.add(new_game)
    await db.commit()
    await db.refresh(new_game)
    return {"game_id": new_game.id, "is_active": new_game.is_active}


@router.post("/game/{game_id}/attempt", response_model=schemas.AttemptResult)
async def make_attempt(
        game_id: int, attempt: schemas.Attempt, db: AsyncSession = Depends(database.get_db),
        current_user: User = Depends(get_current_user)
):
    game = await db.get(models.Game, game_id)
    if not game or not game.is_active:
        raise HTTPException(status_code=404, detail="Game not found or already finished")

    target_word = game.target_word
    if len(attempt.word) != 5:
        raise HTTPException(status_code=400, detail="Word must be 5 letters long")

    correct_positions = [i for i in range(5) if attempt.word[i] == target_word[i]]
    correct_letters = [i for i in range(5) if attempt.word[i] in target_word and attempt.word[i] != target_word[i]]

    # Сохраняем попытку
    new_attempt = models.Attempt(game_id=game_id, word=attempt.word)
    new_attempt.set_correct_positions(correct_positions)  # Сериализуем позиции
    new_attempt.set_correct_letters(correct_letters)  # Сериализуем буквы
    db.add(new_attempt)
    game.attempts += 1

    # Проверка на выигрыш
    game_won = attempt.word == target_word
    if game_won or game.attempts >= 6:
        game.is_active = False
        if game_won:
            current_user.score += 1  # Увеличиваем счет
    await db.commit()

    return {
        "word": attempt.word,
        "correct_positions": new_attempt.get_correct_positions(),  # Десериализуем позиции
        "correct_letters": new_attempt.get_correct_letters(),  # Десериализуем буквы
        "attempts_left": 6 - game.attempts,
        "game_won": game_won,
    }
