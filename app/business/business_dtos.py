from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class BusinessCreateDto(BaseModel):
    name: str = Field(default="someBusiness")
    description: str = Field(default="this is coll business")
    location: str = Field(default="some where on earth")
    contact: str = Field(default="0000 0000 0000")
    fk_business_category_id: int = Field(default=1)


class BusinessPhotoProfileDto(BaseModel):
    photo_url: Optional[str]


class BusinessResponse(BaseModel):
    id: str
    name: str
    description: str
    photo_url: Optional[str] = None
    location: str
    contact: str
    created_at: datetime
    updated_at: datetime
    category: Optional[str] = None
    owner: Optional[str] = None
    rating: Optional[int] = None


class BusinessAllPost(BaseModel):
    id: str
    name: str
    description: str
    photo_url: Optional[str] = None
    location: str
    contact: str
    created_at: datetime
    updated_at: datetime


class BusinessAllPostTest(BaseModel):
    id: str
    name: str
    photo_url: Optional[str] = None
    category: Optional[str] = None


class BusinessEdiDto(BaseModel):
    fk_business_category_id: int