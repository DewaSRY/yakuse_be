from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ArticleCreateDto(BaseModel):
    title: str = Field(default="article title from cool guy")
    description: str = Field(default="some descriptions")
    image_url: str = Field(default="xxx")


class ArticleCreateDto(BaseModel):
    title: str = Field("article title from hot guy")
    description: str = Field("some descriptionss")
    image_url: str = Field("yyy")


class ArticleAuthorInfoDto(BaseModel):
    author_id: str
    fullname: str
    username: str
    author_photo_url: Optional[str]


class ArticleBusinessCategoryDto(BaseModel):
    id: int = Field(1)
    name: str


class ArticleResponseDto(BaseModel):
    id: str
    title: str
    description: str
    image_url: str
    author_info: ArticleAuthorInfoDto
    category: ArticleBusinessCategoryDto
    created_at: datetime
    updated_at: datetime