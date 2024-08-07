import datetime

from pydantic import BaseModel

class UserNeedCreateDto(BaseModel):
    title: str
    description: str

class UserNeedResponseDto(BaseModel):
    title: str
    description: str
    is_visible: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime