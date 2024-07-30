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
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Email already Register"
        )
    return optional.data


@router.get("/login")
async def user_login(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """use to get all users"""

    return jwt_service.create_access_token()
