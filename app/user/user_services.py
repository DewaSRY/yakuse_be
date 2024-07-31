from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from .user_model import UserModel
from . import user_dtos

from app.libs import password_lib
from app.utils import optional


def get_user(db: Session, user_id: int) -> optional.Optional[UserModel, Exception]:
    user_model = db.query(UserModel) \
        .filter(UserModel.id == user_id) \
        .first()
    if not user_model:
        return optional.build(error=Exception("user not found"))
    return optional.build(data=user_model)


def get_user_by_email(db: Session, email: str) -> optional.Optional[UserModel, Exception]:
    user_model = db.query(UserModel) \
        .filter(UserModel.email.like("%{email}%".format(email=email))) \
        .first()
    if user_model:
        return optional.build(data=user_model)
    return optional.build(error=HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="email is not register"
    ))


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[Type[UserModel]]:
    return db.query(UserModel) \
        .offset(skip) \
        .limit(limit) \
        .all()


def create_user(db: Session, user: user_dtos.UserCreateDto) -> optional.Optional[UserModel, Exception]:
    try:
        hashed_password = password_lib.get_password_hash(password=user.password)
        user_model = UserModel(**user.model_dump())
        user_model.password = hashed_password
        db.add(user_model)
        db.commit()
        return optional.build(data=user_model)
    except SQLAlchemyError:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already Register"
        ))


def user_login(db: Session, user: user_dtos.UserLoginPayloadDto) -> optional.Optional[UserModel, Exception]:
    user_optional = get_user_by_email(db, user.email)
    if user_optional.error:
        print("check get email")
        return user_optional
    if not password_lib.verify_password(plain_password=user.password, hashed_password=user_optional.data.password):
        return optional.build(error=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="password not match"
        ))
    return user_optional
