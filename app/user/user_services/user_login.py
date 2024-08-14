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

from .get_by_user_email import get_user_by_email


def user_login(db: Session, user: user_dtos.UserLoginPayloadDto) \
        -> optional.Optional[Type[UserModel], Exception]:
    user_optional = get_user_by_email(db, user.email)
    user_mode = user_optional.data

    if user_optional.error:
        return user_optional
    if not password_lib.verify_password(plain_password=user.password,
                                        hashed_password=user_mode.hash_password):
        return optional.build(error=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password not match"
        ))
    return user_optional
