from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator, field_validator


# class BusinessRatingCreateDto(BaseModel):
#     rating_count: int
#     review_description: str
#     fk_business_id: str

class BusinessRatingCreateDto(BaseModel):
    rating_count: Optional[int] = None
    review_description: str


class BusinessRatingCreateResponseDto(BaseModel):
    id: str
    rating_count: Optional[int] = None
    review_description: str
    fk_business_id: str
    created_at: datetime


class BusinessRatingAllResponseDto(BaseModel):
    id: str
    rating_count: int
    review_description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    business_name: Optional[str] = None
    rater_name: Optional[str] = None


class BusinessRatingDto(BaseModel):
    id: str
    rating_count: int
    review_description: str
    rater_name: Optional[str] = None

    # class Config:
    #     from_attributes = True
