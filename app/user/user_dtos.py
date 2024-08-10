from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class UserCreateDto(BaseModel):
    username: str
    email: str
    password: str
    fullname: str
class UserCreateResponseDto(BaseModel):
    username: str
    email: str

class UserEditProfileDto(BaseModel):
    phone: str
    address: str
    about_me: str
class UserEditResponseDto(BaseModel):
    phone: str
    address: str
    about_me: str

class UserEditPhotoProfileDto(BaseModel):
    photo_url: str

class UserGetProfileDto(BaseModel):
    id: str
    fullname: str
    username: str
    email: str
    password: str
    phone: str
    address: str
    about_me: str
    created_at: datetime
    updated_at: datetime
class UserGetProfilTestDto(BaseModel):
    id: str
    username: str
    email: str
    password: str
    fullname: str
    phone: Optional[str] = None
    address: Optional[str] = None
    photo_url: Optional[str] = None
    about_me: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserLoginPayloadDto(BaseModel):
    email: str
    password: str


class FirebaseLoginDto(BaseModel):
    id_token: str
