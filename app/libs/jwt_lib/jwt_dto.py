from pydantic import BaseModel, Field


class AccessTokenDto(BaseModel):
    detail: str = Field(default="Your user account has been login successfully")
    access_token: str


class TokenPayLoad(BaseModel):
    id: str
