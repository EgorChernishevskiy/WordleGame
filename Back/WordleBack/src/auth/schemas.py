from pydantic import BaseModel


class UserCreate(BaseModel):
    user_name: str
    password: str


class UserOut(BaseModel):
    id: int
    user_name: str
    score: int

    class Config:
        orm_mode = True


class UserScore(BaseModel):
    score: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
