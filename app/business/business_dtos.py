from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field

from app.rating.rating_dtos import BusinessRatingDto


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
    total_rater: Optional[int] = None
    rating_list: List[BusinessRatingDto]

    class Config:
        from_attributes = True


class BusinessCreateWithPhotoDto(BaseModel):
    id: Optional[str]  # Bisa None
    name: str
    description: str
    photo_url: Optional[str] = None  # Bisa None
    location: str
    contact: str
    fk_business_category_id: int = Field(default=1)
    created_at: Optional[datetime] = None  # Bisa None
    updated_at: Optional[datetime] = None  # Bisa None


class BusinessAllPost(BaseModel):
    id: str
    name: str
    photo_url: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[int] = None
    created_at: datetime

class BusinessEdiDto(BaseModel):
    fk_business_category_id: int

class BusinessEditDto(BaseModel):
    name: str = Field(default="someBusiness")
    description: str = Field(default="this is coll business")
    location: str = Field(default="some where on earth")
    contact: str = Field(default="0000 0000 0000")
    fk_business_category_id: int = Field(default=1)
class BusinessEditWithPhotoDto(BaseModel):
    id: Optional[str]  # Bisa None
    name: str
    description: str
    photo_url: Optional[str] = None  # Bisa None
    location: str
    contact: str
    fk_business_category_id: int = Field(default=1)
    updated_at: Optional[datetime] = None  # Bisa None