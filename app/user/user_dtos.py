from pydantic import BaseModel


class UserCreateDto(BaseModel):
    username: str
    email: str
    password: str


class UserCreateResponseDto(BaseModel):
    username: str
    email: str


class UserLoginPayloadDto(BaseModel):
    email: str
    password: str


class FirebaseLoginDto(BaseModel):
    id_token: str
