from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator, field_validator


class BusinessCategoryCreateDto(BaseModel):
    name: str
    describe: str

class BusinessCategoryAllPostResponseDto(BaseModel):
    id: int
    name: str
    describe: str
    created_at: datetime