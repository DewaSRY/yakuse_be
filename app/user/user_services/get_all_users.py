from typing import Type, Optional, Callable
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.user.user_model import UserModel

from app.utils import optional


def get_all_users(db: Session, skip: int = 0, limit: int = 100) \
        -> optional.Optional[list[Type[UserModel]], HTTPException]:
    all_users = db.query(UserModel) \
        .offset(skip).limit(limit) \
        .all()
    if len(all_users) == 0:
        return optional.build(
            error=HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="email is not register"))

    return optional.build(data=all_users)
