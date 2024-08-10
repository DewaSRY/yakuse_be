from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator, field_validator


class BusinessCreateDto(BaseModel):
    name: str
    description: str
    location: str
    contact: str

class BusinessPhotoProfileDto(BaseModel):
    photo_url: str

class BusinessResponse(BaseModel):
    name: str
    description: str
    photo_url: Optional[str] = None
    location: str
    contact: str
    created_at: datetime
    updated_at: datetime

class BusinessAllPost(BaseModel):
    id: str
    name: str
    photo_url: Optional[str] = None    
    rating: Optional[int] = None
    category: Optional[str] = None

class BusinessAllPostTest(BaseModel):
    id: str
    name: str
    photo_url: Optional[str] = None    
    category: Optional[str] = None

class BusinessEdiDto(BaseModel):   
    fk_business_category_id: int