from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserNeedCreateDto(BaseModel):
    title: str = Field(default="some needs from cool guy")
    description: str = Field(default="he is handsome and needs a girl friends")


class UserNeedUpdateDto(BaseModel):
    title: str = Field("some needs from hot guy")
    description: str = Field("he is handsome and needs a woman")
    is_visible: bool = Field(False)


class UserNeedUserInfoDto(BaseModel):
    user_id: str
    owner_username: str = Field("someName")
    user_profile_url: Optional[str] = Field("some url")


class UserNeedBusinessCategoryDto(BaseModel):
    id: int
    name: str


class UserNeedResponseDto(BaseModel):
    id: int
    title: str = Field("some title")
    user_info: UserNeedUserInfoDto
    description: str = Field("some desc")
    is_visible: bool = Field(True)
    category: UserNeedBusinessCategoryDto
    created_at: datetime
    updated_at: datetime
