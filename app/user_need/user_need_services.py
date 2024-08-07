from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from .user_need_dtos import UserNeedCreateDto
from .user_need_model import UserNeeds

from app.utils.optional import Optional, build


def create_user_need_service(db: Session, user_need: UserNeedCreateDto, user_id) -> Optional:
    try:
        user_need_model = UserNeeds(**user_need.model_dump())
        user_need_model.fk_user_id = user_id
        db.add(user_need_model)
        db.commit()
        return build(data=user_need_model)
    except SQLAlchemyError as e:
        return build(error=HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="failed to create user need"))

def get_user_need_by_user_id_service(db: Session, user_id: str) -> list[Type[UserNeeds]]:
    return db.query(UserNeeds).filter(UserNeeds.fk_user_id == user_id).all()

def get_user_need_service(db: Session, skip: int = 0, limit: int = 100) -> list[Type[UserNeeds]]:
    return db.query(UserNeeds).offset(skip).limit(limit).all()
