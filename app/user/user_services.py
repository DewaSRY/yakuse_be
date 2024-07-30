from sqlalchemy.orm import Session
# from sqlalchemy import
from typing import Tuple

from .user_model import UserModel
from . import user_dtos
from app.libs import password_lib
from app.utils import optional


def get_user(db: Session, user_id: int):
    return (db.query(UserModel)
            .filter(UserModel.id == user_id)
            .first())


def get_user_by_email(db: Session, email: str):
    return (db.query(UserModel)
            .filter(UserModel.email.like("%{email}%".format(email=email)))
            .first())


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return (db.query(UserModel)
            .offset(skip)
            .limit(limit)
            .all())


def create_user(db: Session, user: user_dtos.UserCreateDto):
    try:
        hashed_password = password_lib.get_password_hash(password=user.password)
        db_user = UserModel()
        db_user.username = user.username
        db_user.password = hashed_password
        db_user.email = user.email
        db.add(db_user)
        db.commit()
        return optional.build(data=db_user)
    except Exception as e:
        print(e)
        return optional.build(error=e)


def user_login(db: Session, user: user_dtos.UserLoginPayloadDto):
    pass
