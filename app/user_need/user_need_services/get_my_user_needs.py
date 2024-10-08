from typing import Type

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.user_need.user_need_dtos import UserNeedCreateDto, UserNeedUpdateDto
from app.user_need.user_need_model import UserNeeds

from app.utils.optional import Optional, build


def get_my_user_needs(db: Session, user_id: str) -> Optional:
    try:
        user_needs = db.query(UserNeeds) \
            .filter(UserNeeds.fk_user_id==user_id) \
            .order_by(desc(UserNeeds.created_at)).all()

        # user_need_dtos = [user_need.to_response_dto() for user_need in user_needs]

        return build(data=user_needs)
    except SQLAlchemyError as e:
        return build(error=HTTPException(detail=f"{e}", status_code=status.HTTP_404_NOT_FOUND))
