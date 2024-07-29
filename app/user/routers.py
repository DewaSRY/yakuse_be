from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.libs.sql_alchemy_lib import get_db
from . import services, user_dtos

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/", response_model=user_dtos.UserDto)
def create_user(user: user_dtos.UserCreateDto, db: Session = Depends(get_db)):
    """This method use to create user"""
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Email already Register"
        )
    return services.create_user(db=db, user=user)


@router.get("/login", response_model=list[user_dtos.UserDto])
async def user_login(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """use to get all users"""
    return services.get_users(db, skip, limit)
