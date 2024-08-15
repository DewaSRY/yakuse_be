from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.user_need.user_need_model import UserNeeds
from app.user_need import user_need_dtos

from app.utils.optional import Optional, build


def create_user_need(db: Session, user_need: user_need_dtos.UserNeedCreateDto, user_id: str) -> Optional:
    try:
        user_need_model = UserNeeds(
            title=user_need.title,
            description=user_need.description,
            fk_business_category_id=user_need.fk_business_category_id,
            fk_user_id=user_id,
        )

        db.add(user_need_model)
        db.commit()
        db.refresh(user_need_model)

        # user_need_dto = user_need_model.to_response_dto()
        return build(data=user_need_model)
    except SQLAlchemyError as e:
        return build(
            error=HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Failed to create user need. {e}"))
