from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from fastapi import Request

class OptionalOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        # Получаем токен из заголовка запроса или возвращаем None
        authorization: str = request.headers.get("Authorization")
        if authorization:
            return await super().__call__(request)
        return None
