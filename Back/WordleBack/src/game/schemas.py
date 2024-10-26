from pydantic import BaseModel


class GameStart(BaseModel):
    game_id: int
    is_active: bool


class AttemptResult(BaseModel):
    word: str
    correct_positions: list[int]  # Индексы букв на правильных позициях
    correct_letters: list[int]  # Индексы букв, входящих в слово, но не на месте
    attempts_left: int
    game_won: bool


class Attempt(BaseModel):
    word: str
