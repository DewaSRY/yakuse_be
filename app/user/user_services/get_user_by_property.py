from typing import Type, Optional, Callable
from sqlalchemy.orm import Session
from sqlalchemy import BinaryExpression
from fastapi import HTTPException, status
from app.user.user_model import UserModel
from app.utils import optional


def get_user_by_property(
        db: Session, filter_property: Callable[[Type[UserModel]], BinaryExpression[bool]]) \
        -> optional.Optional[Type[UserModel], HTTPException]:
    user_model: Type[UserModel] = db.query(UserModel) \
        .filter(filter_property(UserModel)).first()

    if user_model:
        return optional.build(data=user_model)
    else:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        ))
