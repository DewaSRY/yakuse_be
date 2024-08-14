from typing import Type, Optional, Callable
from sqlalchemy.orm import Session

from fastapi import HTTPException, UploadFile, status

from app.user.user_model import UserModel

from app.utils import optional, find_errr_from_args


def get_user(db: Session, user_id: str) -> optional.Optional[Type[UserModel], Exception]:
    user_model: Type[UserModel] = db.query(UserModel) \
        .filter(UserModel.id == user_id) \
        .first()

    if not user_model:
        return optional.build(error=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"))

    return optional.build(data=user_model)
