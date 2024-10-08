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

# class UserEditWithPhotoDto(BaseModel):
#     id: Optional[str]  # Bisa None
#     name: str
#     omset: float
#     description: str
#     photo_url: Optional[str] = None  # Bisa None
#     location: str
#     contact: str
#     fk_business_category_id: int = Field(default=1)
#     created_at: Optional[datetime] = None  # Bisa None
#     updated_at: Optional[datetime] = None  # Bisa None

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


# DTO untuk menangkap data dari JSON
class ChangePasswordDto(BaseModel):
    old_password: str
    new_password: str

class ChangePasswordResponseDto(BaseModel):
    message : str = Field(default="Password has been changed successfully")
    data: ChangePasswordDto

# class FirebaseLoginDto(BaseModel):
#     id_token: str

class DeleteUserResponseDto(BaseModel):
    detail: str = Field(default="Your user account has been deleted successfully")
    user_id: str
    username: str
    email: str
    