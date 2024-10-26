from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import get_user_from_token
from src.database import get_db
from src.auth.models import User

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#
# async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
#     return await get_user_from_token(token, db)
