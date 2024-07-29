from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi.security import HTTPBearer
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = HTTPBearer()


class TokenData(BaseModel):
    username: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = (datetime.now(timezone.utc) + expires_delta if expires_delta
              else datetime.now(timezone.utc) + timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_jwt_pyload(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        print(payload)
        return TokenData(username=payload)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
