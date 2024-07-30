from pydantic import BaseModel


class AccessTokenDto(BaseModel):
    access_token: str


class TokenPayLoad(BaseModel):
    user_id: str
