from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.user_need.user_need_dtos import UserNeedCreateDto, UserNeedUpdateDto
from app.user_need.user_need_model import UserNeeds

from app.utils.optional import Optional, build


def get_user_need_by_id(db: Session, user_need_id: int) -> Optional:
    try:
        user_need = db.query(UserNeeds) \
            .filter(UserNeeds.id==user_need_id).first()

        # user_need_dto = user_need.to_response_dto()

        return build(data=user_need)
    except SQLAlchemyError as e:
        return build(error=HTTPException(detail=f"{e}", status_code=status.HTTP_404_NOT_FOUND))
