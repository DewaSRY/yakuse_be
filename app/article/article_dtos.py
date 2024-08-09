from datetime import datetime

from pydantic import BaseModel

class ArticleCreateDto(BaseModel):
    title: str
    description: str
    image_url: str

class ArticleResponseDto(BaseModel):
    id: str
    title: str
    description: str
    image_url: str
    created_at: datetime
    updated_at: datetime