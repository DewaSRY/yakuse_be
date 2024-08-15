from typing import Type, Optional, Callable
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from fastapi import HTTPException, UploadFile, status

from app.user.user_model import UserModel

from app.utils import optional, find_errr_from_args


def get_user_profile_by_id(db: Session, user_id: str) -> optional.Optional:
    try:
        user_model=db.query(UserModel) \
            .filter(UserModel.id == user_id).first()
        if user_model is None:
            return optional.build(error=HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"))
        return optional.build(data=user_model)

    except SQLAlchemyError as e:
        db.rollback()
        return optional.build(error=HTTPException(
            status_code=409, detail="Database conflict: " + str(e)))
