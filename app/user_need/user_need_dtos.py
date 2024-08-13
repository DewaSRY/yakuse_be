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


class UserNeedsUserInfoDto(BaseModel):
    user_id: str
    owner_username: str = Field("someName")
    user_profile_url: Optional[str] = Field("some url")


class UserNeedResponseDto(BaseModel):
    id: int
    title: str = Field("some title")
    user_info: UserNeedsUserInfoDto
    description: str = Field("some desc")
    is_visible: bool = Field(True)
    created_at: datetime
    updated_at: datetime
