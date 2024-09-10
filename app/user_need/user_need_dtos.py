from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserNeedCreateDto(BaseModel):
    title: str = Field(default="some needs from cool guy")
    description: str = Field(default="he is handsome and needs a girl friends")
    fk_business_category_id: int = Field(default=1)


class UserNeedUpdateDto(BaseModel):
    title: str = Field("some needs from hot guy")
    description: str = Field("he is handsome and needs a woman")
    fk_business_category_id: int
    is_visible: bool

class UserNeedUserInfoDto(BaseModel):
    user_id: str
    fullname: str
    username: str
    user_profile_url: Optional[str]


class UserNeedBusinessCategoryDto(BaseModel):
    id: int = Field(1)
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



class TestUserNeedResponseDto(BaseModel):
    id: int
    title: str = Field("some title")
    fk_user_id: str
    description: str = Field("some desc")
    is_visible: bool = Field(True)
    fk_business_category_id: int
    created_at: datetime
    updated_at: datetime