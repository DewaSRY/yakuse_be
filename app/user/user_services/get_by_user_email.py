from typing import Type, Optional, Callable
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import BinaryExpression
from fastapi import HTTPException, UploadFile, status

from app.libs.images_service import create_image_service

from app.user.user_model import UserModel
from app.user import user_dtos

from app.libs import password_lib
from app.utils import optional, find_errr_from_args
from app.libs.jwt_lib import jwt_dto, jwt_service

from .get_user_by_property import get_user_by_property


def get_user_by_email(db: Session, user_email: str) \
        -> optional.Optional[Type[UserModel], HTTPException]:
    def user_filter(user_model: Type[UserModel]):
        return user_model.email.like(f"{user_email}")

    user_opt = get_user_by_property(db=db, filter_property=user_filter)

    if user_opt.data:
        return user_opt

    return optional.build(error=HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="email is not register"
    ))
