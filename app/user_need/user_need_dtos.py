from datetime import datetime

from pydantic import BaseModel

class UserNeedCreateDto(BaseModel):
    title: str
    description: str

class UserNeedUpdateDto(BaseModel):
    title: str
    description: str
    is_visible: bool

class UserNeedResponseDto(BaseModel):
    title: str
    description: str
    is_visible: bool
    created_at: datetime
    updated_at: datetime