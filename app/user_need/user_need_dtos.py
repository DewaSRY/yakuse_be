from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserNeedCreateDto(BaseModel):
    title: str = Field(default="some needs from cool guy")
    description: str = Field(default="he is handsome and needs a girl friends")


class UserNeedUpdateDto(BaseModel):
    title: str
    description: str
    is_visible: bool


class UserNeedsUserInfoDto(BaseModel):
    owner_username: str = Field("someName")
    user_profile_url: Optional[str] = Field("some url")


class UserNeedResponseDto(BaseModel):
    id: int
    title: str
    user_info: UserNeedsUserInfoDto
    description: str
    is_visible: bool
    created_at: datetime
    updated_at: datetime
