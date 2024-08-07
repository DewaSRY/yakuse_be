import datetime

from pydantic import BaseModel, validator, field_validator


class BusinessCreateDto(BaseModel):
    name: str
    description: str
    photo_url: str
    location: str
    contact: str


class BusinessResponse(BaseModel):
    name: str
    description: str
    photo_url: str
    location: str
    contact: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
