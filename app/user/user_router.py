from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session

from app.libs.sql_alchemy_lib import get_db
from app.libs.jwt_lib import jwt_service, jwt_dto

from . import user_services, user_dtos

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/", response_model=user_dtos.UserCreateResponseDto)
def create_user(user: user_dtos.UserCreateDto, db: Session = Depends(get_db)):
    """This method use to create user"""
    optional = user_services.create_user(db, user)
    if optional.error:
        raise optional.error
    return optional.data


@router.post("/login", response_model=jwt_dto.AccessTokenDto)
async def user_login(user: user_dtos.UserLoginPayloadDto, db: Session = Depends(get_db)):
    """use to get all users"""
    user_optional = user_services.user_login(db=db, user=user)
    if user_optional.error:
        raise user_optional.error
    user_ditch = dict([
        ("user_id", user_optional.data.id)
    ])
    return jwt_service.create_access_token(user_ditch)
