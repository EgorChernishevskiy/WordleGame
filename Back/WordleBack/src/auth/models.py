from sqlalchemy import Column, Integer, String, Float

from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True, nullable=False)
    password_hashed = Column(String, nullable=False)
    score = Column(Integer, default=0)
    games = relationship("Game", back_populates="user")  # Связь с играми

    games_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)