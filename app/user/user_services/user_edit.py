from typing import Type, Optional, Callable
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile, status

from app.user.user_model import UserModel
from app.user import user_dtos

from app.utils import optional, find_errr_from_args


def user_edit(db: Session, user: user_dtos.UserEditProfileDto, user_id: str) \
        -> optional.Optional[Type[UserModel], HTTPException]:
    try:
        user_model: Type[UserModel] = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_model:
            for field, value in user.dict().items():
                setattr(user_model, field, value)

            db.commit()
            db.refresh(user_model)
            return optional.build(data=user_model)
        else:
            return optional.build(
                error=HTTPException(status_code=404, detail="User not found"))

    except SQLAlchemyError as e:
        db.rollback()
        return optional.build(
            error=HTTPException(status_code=409, detail="Database conflict: " + str(e)))
