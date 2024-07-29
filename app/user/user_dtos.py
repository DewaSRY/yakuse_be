from pydantic import BaseModel


class UserBaseDto(BaseModel):
    email: str


class UserCreateDto(UserBaseDto):
    password: str


class UserDto(UserBaseDto):
    id: int
    is_active: bool

    class Config:
        from_attributes = True  # Updated from 'orm_mode'
