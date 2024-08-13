from datetime import datetime

from pydantic import BaseModel, Field

class ArticleCreateDto(BaseModel):
    title: str = Field(default="some articles from cool guy")
    description: str = Field(default="this is description")
    image_url: str = Field(default="xxx")

class ArticleResponseDto(BaseModel):
    id: str
    title: str
    description: str
    image_url: str
    created_at: datetime
    updated_at: datetime