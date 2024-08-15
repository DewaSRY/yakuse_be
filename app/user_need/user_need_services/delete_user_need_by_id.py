from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.user_need.user_need_dtos import UserNeedCreateDto, UserNeedUpdateDto
from app.user_need.user_need_model import UserNeeds

from app.utils.optional import Optional, build


def delete_user_need_by_id(db: Session, user_id: str, user_need_id: str):
    try:
        user_need_model = db.query(UserNeeds).filter(UserNeeds.fk_user_id == user_id).filter(
            UserNeeds.id == user_need_id).first()
        if user_need_model is None:
            raise HTTPException(status_code=404, detail='User need not found.')
        db.query(UserNeeds) \
            .filter(UserNeeds.fk_user_id == user_id) \
            .filter(UserNeeds.id == user_need_id).delete()
        db.commit()
        return
    except SQLAlchemyError as e:
        return build(error=HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to delete user need."))
