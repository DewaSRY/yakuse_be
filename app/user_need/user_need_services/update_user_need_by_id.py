from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.user_need.user_need_dtos import UserNeedCreateDto, UserNeedUpdateDto
from app.user_need.user_need_model import UserNeeds

from app.utils.optional import Optional, build


def update_user_need_by_id(db: Session, user_id: str, user_need_id: str,
                                   user_need_update: UserNeedUpdateDto) -> Optional:
    try:
        user_need_model = db.query(UserNeeds).filter(UserNeeds.fk_user_id == user_id).filter(
            UserNeeds.id == user_need_id).first()
        if user_need_model is None:
            raise HTTPException(status_code=404, detail='User need not found.')
        user_need_model.title = user_need_update.title
        user_need_model.description = user_need_update.description
        user_need_model.fk_business_category_id = user_need_update.fk_business_category_id
        user_need_model.is_visible = user_need_update.is_visible
        db.add(user_need_model)
        db.commit()
        return build(data=user_need_model)
    except SQLAlchemyError as e:
        return build(error=HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to update user need."))