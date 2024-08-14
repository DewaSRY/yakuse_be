from typing import Type, Optional, Callable
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import BinaryExpression
from fastapi import HTTPException, UploadFile, status

from app.user.user_model import UserModel
from app.user import user_dtos

from app.libs import password_lib
from app.utils import optional


def create_user(db: Session, user: user_dtos.UserCreateDto) -> optional.Optional[UserModel, Exception]:
    try:
        user_model = UserModel()
        user_model.email = user.email
        user_model.fullname = user.fullname
        user_model.username = user.username
        user_model.hash_password = password_lib.get_password_hash(password=user.password)

        db.add(user_model)
        db.commit()
        return optional.build(data=user_model)
    except SQLAlchemyError as e:
        # print(e)
        return optional.build(error=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email already use"))
