from datetime import datetime

from pydantic import BaseModel


class UserCreateDto(BaseModel):
    username: str
    email: str
    password: str
    fullname: str

class UserEditProfileDto(BaseModel):
    phone: str
    about_me: str

class UserEditResponseDto(BaseModel):
    phone: str
    about_me: str

class UserGetProfileDto(BaseModel):
    id: str
    fullname: str
    username: str
    email: str
    password: str
    phone: str
    about_me: str
    created_at: datetime
    updated_at: datetime

class UserGetProfilTestDto(BaseModel):
    username: str
    email: str
    password: str
    fullname: str
    created_at: datetime
    updated_at: datetime

class UserCreateResponseDto(BaseModel):
    username: str
    email: str


class UserLoginPayloadDto(BaseModel):
    email: str
    password: str


class FirebaseLoginDto(BaseModel):
    id_token: str
