from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.user_need.user_need_dtos import UserNeedCreateDto, UserNeedUpdateDto
from app.user_need.user_need_model import UserNeeds

from app.utils.optional import Optional, build


def get_all_user_needs(db: Session, skip: int = 0, limit: int = 100) -> list[Type[UserNeeds]]:
    try:
        user_needs = db.query(UserNeeds).offset(skip).limit(limit).all()
        return build(data=user_needs)
    except SQLAlchemyError as e:
        return build(error=HTTPException(detail=f"{e}"))