from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserCreateDto(BaseModel):
    username: str = Field(default="username")
    email: EmailStr = Field(default="Example@Example.com")
    password: str = Field(default="somePassword")
    fullname: str = Field(default="SomeFullName")


class UserCreateResponseDto(BaseModel):
    id: str
    username: str
    email: str
    fullname: str
    phone: Optional[str] = None
    address: Optional[str] = None
    photo_url: Optional[str] = None
    # about_me: Optional[str] = None
    about_me_list: list[str]
    created_at: datetime
    updated_at: datetime


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


# class UserGetProfileDto(BaseModel):
#     id: str
#     fullname: str
#     username: str
#     email: str
#     password: str
#     phone: str
#     address: str
#     about_me: str
#     created_at: datetime
#     updated_at: datetime


# class UserGetProfilTestDto(BaseModel):
#     id: str
#     username: str
#     email: str
#     hash_password: str
#     fullname: str
#     phone: Optional[str] = None
#     address: Optional[str] = None
#     photo_url: Optional[str] = None
#     about_me: Optional[str] = None
#     created_at: datetime
#     updated_at: datetime


class UserLoginPayloadDto(BaseModel):
    email: EmailStr = Field(default="Example@Example.com")
    password: str = Field(default="somePassword")

# class FirebaseLoginDto(BaseModel):
#     id_token: str
