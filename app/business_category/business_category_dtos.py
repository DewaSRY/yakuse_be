from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator, field_validator, Field


class BusinessCategoryCreateDto(BaseModel):
    name: str = Field(default="kuliner")
    describe: str = Field(default="Kuliner adalah segala hal yang berhubungan dengan makanan dan minuman")


class BusinessCategoryAllPostResponseDto(BaseModel):
    id: int
    name: str
    describe: str
    created_at: datetime
