from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from .user_need_dtos import UserNeedCreateDto, UserNeedUpdateDto
from .user_need_model import UserNeeds

from app.utils.optional import Optional, build


def create_user_need_service(db: Session, user_need: UserNeedCreateDto, user_id: str) -> Optional:
    try:
        user_need_model = UserNeeds(**user_need.model_dump())
        user_need_model.fk_user_id = user_id
        db.add(user_need_model)
        db.commit()
        return build(data=user_need_model)
    except SQLAlchemyError as e:
        return build(error=HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to create user need."))

def get_user_need_service(db: Session, skip: int = 0, limit: int = 100) -> list[Type[UserNeeds]]:
    return db.query(UserNeeds).offset(skip).limit(limit).all()

def get_user_need_by_user_id_service(db: Session, user_id: str) -> list[Type[UserNeeds]]:
    return db.query(UserNeeds).filter(UserNeeds.fk_user_id == user_id).all()

def get_user_need_by_id_service(db: Session, user_need_id: str) -> Type[UserNeeds]:
    return db.query(UserNeeds).filter(UserNeeds.id == user_need_id).first()

def update_user_need_by_id_service(db: Session, user_id: str, user_need_id: str, user_need_update: UserNeedUpdateDto) -> Optional:
    try:
        user_need_model = db.query(UserNeeds).filter(UserNeeds.fk_user_id == user_id).filter(UserNeeds.id == user_need_id).first()
        if user_need_model is None:
            raise HTTPException(status_code=404, detail='User need not found.')
        user_need_model.title = user_need_update.title
        user_need_model.description = user_need_update.description
        user_need_model.is_visible = user_need_update.is_visible
        db.add(user_need_model)
        db.commit()
        return build(data=user_need_model)
    except SQLAlchemyError as e:
        return build(error=HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to update user need."))

# def hide_user_need_by_id_service(db: Session, user_need_id: str):
#     return db.query(UserNeeds).get(user_need_id)


def delete_user_need_by_id_service(db: Session, user_id: str, user_need_id: str):
    user_need_model = db.query(UserNeeds).filter(UserNeeds.fk_user_id == user_id).filter(UserNeeds.id == user_need_id).first()
    if user_need_model is None:
        raise HTTPException(status_code=404, detail='User need not found.')
    db.query(UserNeeds).filter(UserNeeds.fk_user_id == user_id).filter(UserNeeds.id == user_need_id).delete()
    db.commit()