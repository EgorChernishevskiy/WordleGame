import json

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    target_word = Column(String, nullable=False)  # Загаданное слово
    attempts = Column(Integer, default=0)  # Количество попыток
    is_active = Column(Boolean, default=True)  # Статус игры

    user = relationship("User", back_populates="games")  # Связь с пользователем
    attempts_list = relationship("Attempt", back_populates="game")  # Связь с попытками


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    word = Column(String, nullable=False)  # Слово, введенное пользователем
    correct_positions = Column(String)  # Буквы на верных позициях, в формате JSON
    correct_letters = Column(String)  # Буквы, входящие в слово, но не на своих местах, в формате JSON

    game = relationship("Game", back_populates="attempts_list")

    def set_correct_positions(self, positions):
        self.correct_positions = json.dumps(positions)  # Сериализация списка в строку

    def get_correct_positions(self):
        return json.loads(self.correct_positions) if self.correct_positions else []  # Десериализация строки в список

    def set_correct_letters(self, letters):
        self.correct_letters = json.dumps(letters)  # Сериализация списка в строку

    def get_correct_letters(self):
        return json.loads(self.correct_letters) if self.correct_letters else []  # Десериализация строки в список
